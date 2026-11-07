import React, { useState, useEffect } from 'react';
import { BookOpen, Terminal, CheckCircle2, XCircle, Award, RotateCcw, Play, Clock, Sparkles } from 'lucide-react';
import confetti from 'canvas-confetti';
import { MathContent } from '../utils/mathRenderer';

export default function QuizTab() {
  const [subTab, setSubTab] = useState('mcq');

  // MCQ State
  const [subject, setSubject] = useState('Programming');
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState('Intermediate');
  const [numQuestions, setNumQuestions] = useState(3);
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState(null);
  const [userAnswers, setUserAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(0);
  const [quizHistory, setQuizHistory] = useState([]);

  // Coding Challenges State
  const [challengesData, setChallengesData] = useState({});
  const [codingSubject, setCodingSubject] = useState('Programming');
  const [selectedChallengeIdx, setSelectedChallengeIdx] = useState(0);
  const [userCode, setUserCode] = useState('');
  const [evalLoading, setEvalLoading] = useState(false);
  const [evalResult, setEvalResult] = useState(null);
  const [codingHistory, setCodingHistory] = useState([]);

  // Load Initial History & Challenges
  useEffect(() => {
    fetchQuizHistory();
    fetchChallenges();
    fetchCodingHistory();
  }, []);

  const fetchQuizHistory = async () => {
    try {
      const res = await fetch('/api/quiz/history?limit=5');
      const data = await res.json();
      setQuizHistory(data.history || []);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchChallenges = async () => {
    try {
      const res = await fetch('/api/challenges');
      const data = await res.json();
      setChallengesData(data.challenges || {});
      const initialSubjChallenges = data.challenges?.['Programming'] || [];
      if (initialSubjChallenges.length > 0) {
        setUserCode(initialSubjChallenges[0].starter_code);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchCodingHistory = async () => {
    try {
      const res = await fetch('/api/challenges/history?limit=5');
      const data = await res.json();
      setCodingHistory(data.history || []);
    } catch (e) {
      console.error(e);
    }
  };

  const handleGenerateQuiz = async () => {
    setLoading(true);
    setQuestions(null);
    setUserAnswers({});
    setSubmitted(false);

    try {
      const query = new URLSearchParams({
        subject,
        topic: topic.trim(),
        level,
        num_questions: numQuestions
      });
      const res = await fetch(`/api/quiz/generate?${query.toString()}`);
      const data = await res.json();
      setQuestions(data.questions || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitQuiz = async () => {
    if (!questions) return;
    let score = 0;
    questions.forEach((q, idx) => {
      if (userAnswers[idx] === q.correct) {
        score += 1;
      }
    });

    setQuizScore(score);
    setSubmitted(true);

    const pct = Math.round((score / questions.length) * 100);
    if (pct >= 80) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }

    try {
      await fetch('/api/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject,
          topic: topic || 'Core Concepts',
          score,
          total_questions: questions.length,
          details: userAnswers
        })
      });
      fetchQuizHistory();
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunCodingChallenge = async () => {
    const activeList = challengesData[codingSubject] || [];
    const activeChallenge = activeList[selectedChallengeIdx];
    if (!activeChallenge) return;

    setEvalLoading(true);
    setEvalResult(null);

    try {
      const res = await fetch('/api/challenges/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: userCode,
          challenge: activeChallenge,
          subject: codingSubject
        })
      });
      const data = await res.json();
      setEvalResult(data);
      fetchCodingHistory();
    } catch (err) {
      setEvalResult({ success: false, error: err.message });
    } finally {
      setEvalLoading(false);
    }
  };

  const activeChallengeList = challengesData[codingSubject] || [];
  const currentChallenge = activeChallengeList[selectedChallengeIdx];

  return (
    <div className="space-y-6">
      {/* Sub Tab Switcher */}
      <div className="flex gap-2 p-1 bg-slate-900/80 border border-white/10 rounded-xl w-fit">
        <button
          onClick={() => setSubTab('mcq')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'mcq'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" /> Multiple-Choice Conceptual Quiz
        </button>
        <button
          onClick={() => setSubTab('coding')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'coding'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Terminal className="w-3.5 h-3.5" /> Live Coding Challenges & Sandbox
        </button>
      </div>

      {/* ========================================================= */}
      {/* SUB TAB 1: MCQ QUIZ                                      */}
      {/* ========================================================= */}
      {subTab === 'mcq' && (
        <div className="space-y-6">
          <div className="glass-card p-6">
            <h4 className="text-sm font-bold text-white mb-4">Quiz Generation Setup</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Academic Discipline
                </label>
                <select
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  className="w-full text-xs"
                >
                  <option>Programming</option>
                  <option>Mathematics</option>
                  <option>Machine Learning</option>
                  <option>Deep Learning</option>
                  <option>NLP</option>
                  <option>Data Science</option>
                  <option>Computer Architecture & Microprocessors</option>
                  <option>Physics & Engineering Sciences</option>
                  <option>Electrical & Electronics Engineering</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Topic / Sub-field (Optional)
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g. Recursion, Loss Functions"
                  className="w-full text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Difficulty
                </label>
                <select
                  value={level}
                  onChange={(e) => setLevel(e.target.value)}
                  className="w-full text-xs"
                >
                  <option>Beginner</option>
                  <option>Intermediate</option>
                  <option>Advanced</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Questions
                </label>
                <select
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(Number(e.target.value))}
                  className="w-full text-xs"
                >
                  <option value={3}>3 Questions</option>
                  <option value={4}>4 Questions</option>
                  <option value={5}>5 Questions</option>
                </select>
              </div>
            </div>

            <button
              onClick={handleGenerateQuiz}
              disabled={loading}
              className="btn-primary mt-4 py-2 px-5 text-xs"
            >
              <Sparkles className="w-3.5 h-3.5" />
              {loading ? 'Generating Questions...' : 'Generate Interactive Quiz'}
            </button>
          </div>

          {/* Active Questions Panel */}
          {questions && questions.length > 0 && (
            <div className="space-y-6">
              {!submitted ? (
                <div className="space-y-5">
                  {questions.map((q, qIdx) => (
                    <div key={qIdx} className="glass-card p-6 space-y-4">
                      <div className="text-sm font-bold text-white flex gap-2">
                        <span className="text-indigo-400">Q{qIdx + 1}.</span>
                        <MathContent content={q.question} />
                      </div>

                      <div className="space-y-2 pt-2">
                        {q.options.map((opt, oIdx) => (
                          <label
                            key={oIdx}
                            onClick={() => setUserAnswers((prev) => ({ ...prev, [qIdx]: oIdx }))}
                            className={`flex items-center gap-3 p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                              userAnswers[qIdx] === oIdx
                                ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-sm'
                                : 'bg-slate-900/40 border-white/5 text-slate-300 hover:bg-white/5'
                            }`}
                          >
                            <input
                              type="radio"
                              name={`q_${qIdx}`}
                              checked={userAnswers[qIdx] === oIdx}
                              onChange={() => {}}
                              className="accent-indigo-500"
                            />
                            <span className="font-semibold">{String.fromCharCode(65 + oIdx)})</span>
                            <MathContent content={opt} />
                          </label>
                        ))}
                      </div>
                    </div>
                  ))}

                  <button
                    onClick={handleSubmitQuiz}
                    disabled={Object.keys(userAnswers).length < questions.length}
                    className="btn-primary py-3 px-6 w-full text-sm font-bold"
                  >
                    🏁 Submit Quiz for Instant Grading ({Object.keys(userAnswers).length}/{questions.length} answered)
                  </button>
                </div>
              ) : (
                /* Results Review Panel */
                <div className="space-y-6">
                  <div className="glass-card p-8 text-center border-indigo-500/40 bg-indigo-950/20">
                    <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
                      Assessment Score
                    </div>
                    <div className="text-5xl font-extrabold text-sky-400 mb-2">
                      {quizScore} / {questions.length}
                    </div>
                    <div className="text-base font-bold text-emerald-400 mb-4">
                      {Math.round((quizScore / questions.length) * 100)}% Conceptual Mastery
                    </div>
                    <button onClick={handleGenerateQuiz} className="btn-secondary text-xs">
                      <RotateCcw className="w-3.5 h-3.5" /> Retake or Generate New Quiz
                    </button>
                  </div>

                  <div className="space-y-4">
                    <h4 className="text-sm font-bold text-white">📋 Question-by-Question Solution Review</h4>
                    {questions.map((q, qIdx) => {
                      const userChoice = userAnswers[qIdx];
                      const isCorrect = userChoice === q.correct;

                      return (
                        <div
                          key={qIdx}
                          className={`glass-card p-5 border ${
                            isCorrect ? 'border-emerald-500/40' : 'border-rose-500/40'
                          }`}
                        >
                          <div className="flex items-start justify-between gap-3 mb-3">
                            <div className="text-sm font-bold text-white flex gap-2">
                              <span>Q{qIdx + 1}.</span>
                              <MathContent content={q.question} />
                            </div>
                            <span
                              className={`px-2.5 py-0.5 rounded-full text-xs font-bold shrink-0 flex items-center gap-1 ${
                                isCorrect
                                  ? 'bg-emerald-500/15 text-emerald-300'
                                  : 'bg-rose-500/15 text-rose-300'
                              }`}
                            >
                              {isCorrect ? (
                                <>
                                  <CheckCircle2 className="w-3 h-3" /> Correct
                                </>
                              ) : (
                                <>
                                  <XCircle className="w-3 h-3" /> Incorrect
                                </>
                              )}
                            </span>
                          </div>

                          <div className="space-y-1.5 text-xs">
                            {q.options.map((opt, oIdx) => (
                              <div
                                key={oIdx}
                                className={`p-2 rounded-lg ${
                                  oIdx === q.correct
                                    ? 'bg-emerald-500/15 text-emerald-200 font-semibold border border-emerald-500/30'
                                    : oIdx === userChoice && !isCorrect
                                    ? 'bg-rose-500/15 text-rose-300 font-semibold border border-rose-500/30'
                                    : 'text-slate-400'
                                }`}
                              >
                                {String.fromCharCode(65 + oIdx)}) <MathContent content={opt} />
                              </div>
                            ))}
                          </div>

                          <div className="mt-4 pt-3 border-t border-white/5 text-xs text-slate-300 bg-white/5 p-3 rounded-lg">
                            <span className="font-bold text-indigo-400">💡 Explanation: </span>
                            <MathContent content={q.explanation} />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Past Quizzes List */}
          {quizHistory.length > 0 && (
            <div className="glass-card p-6 mt-8">
              <h4 className="text-sm font-bold text-white mb-3">📊 Your Recent Quiz Records</h4>
              <div className="space-y-2 text-xs">
                {quizHistory.map((qh, i) => (
                  <div
                    key={i}
                    className="flex justify-between items-center p-3 rounded-lg bg-slate-900/50 border border-white/5"
                  >
                    <div>
                      <strong className="text-white">{qh.subject}</strong> — {qh.topic}
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-sky-400 font-bold">
                        {qh.score}/{qh.total_questions} ({qh.percentage}%)
                      </span>
                      <span className="text-slate-500 text-[11px]">
                        {qh.timestamp?.slice(0, 10)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* SUB TAB 2: LIVE CODING CHALLENGES                         */}
      {/* ========================================================= */}
      {subTab === 'coding' && (
        <div className="space-y-6">
          <div className="glass-card p-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Select Discipline
                </label>
                <select
                  value={codingSubject}
                  onChange={(e) => {
                    const newSubj = e.target.value;
                    setCodingSubject(newSubj);
                    setSelectedChallengeIdx(0);
                    const list = challengesData[newSubj] || [];
                    if (list.length > 0) setUserCode(list[0].starter_code);
                    setEvalResult(null);
                  }}
                  className="w-full text-xs"
                >
                  {Object.keys(challengesData).map((s) => (
                    <option key={s}>{s}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Select Coding Challenge
                </label>
                <select
                  value={selectedChallengeIdx}
                  onChange={(e) => {
                    const idx = Number(e.target.value);
                    setSelectedChallengeIdx(idx);
                    if (activeChallengeList[idx]) {
                      setUserCode(activeChallengeList[idx].starter_code);
                    }
                    setEvalResult(null);
                  }}
                  className="w-full text-xs"
                >
                  {activeChallengeList.map((ch, idx) => (
                    <option key={idx} value={idx}>
                      {ch.title}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {currentChallenge && (
              <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 space-y-2">
                <div className="text-sm font-bold text-sky-400">📌 Problem: {currentChallenge.title}</div>
                <p className="text-xs text-slate-300 leading-relaxed">{currentChallenge.description}</p>
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5 font-mono">
                solution.py (Python 3.13)
              </label>
              <textarea
                rows={10}
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                className="w-full font-mono text-xs md:text-sm bg-slate-950 p-4 text-emerald-300 border-slate-800 leading-relaxed"
                spellCheck={false}
              />
            </div>

            <button
              onClick={handleRunCodingChallenge}
              disabled={evalLoading}
              className="btn-primary py-2.5 px-6 text-xs font-bold"
            >
              <Play className="w-4 h-4 fill-white" />
              {evalLoading ? 'Executing Test Cases in Sandbox...' : 'Run & Verify Against Test Cases'}
            </button>
          </div>

          {/* Test Case Evaluation Results */}
          {evalResult && (
            <div className="glass-card p-6 space-y-4">
              <div className="flex justify-between items-center pb-2 border-b border-white/10">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <Award className="w-4 h-4 text-indigo-400" />
                  Test Case Evaluation Results
                </h4>
                {evalResult.execution_time_ms && (
                  <span className="text-xs text-slate-400 flex items-center gap-1 font-mono">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    {evalResult.execution_time_ms} ms
                  </span>
                )}
              </div>

              {evalResult.all_passed ? (
                <div className="p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <strong>All Test Cases Passed! Your algorithmic solution is correct and verified.</strong>
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
                  <XCircle className="w-4 h-4" />
                  <span>Some test cases failed or runtime error occurred. Review the breakdown below.</span>
                </div>
              )}

              {evalResult.results && (
                <div className="space-y-2">
                  {evalResult.results.map((tc, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border text-xs flex justify-between items-center font-mono ${
                        tc.passed
                          ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
                          : 'bg-rose-950/20 border-rose-500/30 text-rose-300'
                      }`}
                    >
                      <div className="space-y-0.5">
                        <div>
                          <strong>Test Case {idx + 1}:</strong> {tc.passed ? '✅ Passed' : '❌ Failed'}
                        </div>
                        <div className="text-[11px] text-slate-400">
                          Input: <code>{JSON.stringify(tc.input)}</code>
                        </div>
                      </div>
                      <div className="text-right text-[11px]">
                        <div>Expected: <code>{JSON.stringify(tc.expected)}</code></div>
                        <div>Actual: <code>{JSON.stringify(tc.actual)}</code></div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Coding Challenge History */}
          {codingHistory.length > 0 && (
            <div className="glass-card p-6">
              <h4 className="text-sm font-bold text-white mb-3">📜 Past Coding Submissions</h4>
              <div className="space-y-2 text-xs">
                {codingHistory.map((ca, i) => (
                  <div
                    key={i}
                    className="flex justify-between items-center p-3 rounded-lg bg-slate-900/50 border border-white/5"
                  >
                    <div>
                      <strong className="text-white">{ca.challenge_name}</strong> ({ca.subject})
                    </div>
                    <div className="flex items-center gap-4">
                      <span className={ca.passed === 1 ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}>
                        {ca.passed === 1 ? '✅ Passed' : '❌ Failed'} ({ca.execution_time_ms} ms)
                      </span>
                      <span className="text-slate-500 text-[11px]">
                        {ca.timestamp?.slice(0, 10)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
