import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Terminal,
  CheckCircle2,
  XCircle,
  Award,
  RotateCcw,
  Play,
  Clock,
  Sparkles,
  ChevronLeft,
  ChevronRight,
  HelpCircle,
  BarChart3,
  Check,
  AlertCircle
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { MathContent } from '../utils/mathRenderer';

export default function QuizTab({ onRefreshStats }) {
  const [subTab, setSubTab] = useState('mcq');

  // MCQ State
  const [subject, setSubject] = useState('Programming');
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState('Intermediate');
  const [numQuestions, setNumQuestions] = useState(3);
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState(null);
  const [currentQIdx, setCurrentQIdx] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(0);
  const [quizHistory, setQuizHistory] = useState([]);

  // Active Timer state (in seconds)
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [timerRunning, setTimerRunning] = useState(false);

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

  // Timer Tick
  useEffect(() => {
    let interval = null;
    if (timerRunning && !submitted) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [timerRunning, submitted]);

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
    setCurrentQIdx(0);
    setTimerSeconds(0);
    setTimerRunning(false);

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
      setTimerRunning(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (qIdx, opt) => {
    if (submitted) return;
    setUserAnswers((prev) => ({
      ...prev,
      [qIdx]: opt
    }));
  };

  const handleSubmitQuiz = async () => {
    if (!questions) return;
    setTimerRunning(false);

    let score = 0;
    questions.forEach((q, idx) => {
      if (userAnswers[idx] === q.correct) {
        score += 1;
      }
    });

    setQuizScore(score);
    setSubmitted(true);

    const pct = Math.round((score / questions.length) * 100);
    if (pct >= 70) {
      confetti({
        particleCount: 90,
        spread: 80,
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
      if (onRefreshStats) onRefreshStats();
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
      if (onRefreshStats) onRefreshStats();
    } catch (err) {
      setEvalResult({ success: false, error: err.message });
    } finally {
      setEvalLoading(false);
    }
  };

  const formatTimer = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const activeChallengeList = challengesData[codingSubject] || [];
  const currentChallenge = activeChallengeList[selectedChallengeIdx];

  const totalAnswered = Object.keys(userAnswers).length;
  const progressPct = questions ? Math.round((totalAnswered / questions.length) * 100) : 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      {/* Sub Tab Switcher */}
      <div className="flex gap-2 p-1 bg-[#0D1222] border border-white/10 rounded-xl w-fit">
        <button
          onClick={() => setSubTab('mcq')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'mcq'
              ? 'bg-[#7867FF] text-white shadow-lg shadow-[#7867FF]/30'
              : 'text-[#A1AEC4] hover:text-white'
          }`}
        >
          <BookOpen className="w-4 h-4" /> Multiple-Choice Conceptual Quiz
        </button>
        <button
          onClick={() => setSubTab('coding')}
          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
            subTab === 'coding'
              ? 'bg-[#7867FF] text-white shadow-lg shadow-[#7867FF]/30'
              : 'text-[#A1AEC4] hover:text-white'
          }`}
        >
          <Terminal className="w-4 h-4" /> Live Coding Challenges & Sandbox
        </button>
      </div>

      {/* ========================================================= */}
      {/* SUB TAB 1: MCQ QUIZ                                      */}
      {/* ========================================================= */}
      {subTab === 'mcq' && (
        <div className="space-y-6">
          {/* Generation Form */}
          <div className="glass-card p-6">
            <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#22C8E5]" />
              Generate Academic Practice Quiz
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Academic Discipline
                </label>
                <select
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  className="w-full text-xs bg-[#0D1222]"
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
                  Specific Topic (Optional)
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g. Recursion, CNNs, 8086"
                  className="w-full text-xs bg-[#0D1222]"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Difficulty Level
                </label>
                <select
                  value={level}
                  onChange={(e) => setLevel(e.target.value)}
                  className="w-full text-xs bg-[#0D1222]"
                >
                  <option>Beginner</option>
                  <option>Intermediate</option>
                  <option>Advanced</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Questions Count
                </label>
                <select
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(Number(e.target.value))}
                  className="w-full text-xs bg-[#0D1222]"
                >
                  <option value={3}>3 Questions</option>
                  <option value={5}>5 Questions</option>
                  <option value={10}>10 Questions</option>
                </select>
              </div>
            </div>

            <div className="mt-4 flex justify-end">
              <button
                onClick={handleGenerateQuiz}
                disabled={loading}
                className="btn-primary py-2.5 px-6 text-xs font-semibold"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>{loading ? 'Synthesizing Questions...' : 'Start Practice Quiz'}</span>
              </button>
            </div>
          </div>

          {/* Active Quiz Card */}
          {questions && questions.length > 0 && (
            <div className="glass-card p-6 space-y-6 animate-slide-up border-[#7867FF]/30">
              {/* Quiz Header Bar: Progress, Question Counter, Timer */}
              <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-white/10">
                <div className="flex items-center gap-3">
                  <div className="px-3 py-1 rounded-full bg-[#7867FF]/20 border border-[#7867FF]/35 text-[#7867FF] text-xs font-bold">
                    Question {currentQIdx + 1} of {questions.length}
                  </div>
                  <span className="text-xs text-slate-400">
                    {totalAnswered} of {questions.length} answered
                  </span>
                </div>

                {/* Timer Display */}
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#0D1222] border border-white/10 text-xs font-mono font-bold text-[#22C8E5]">
                  <Clock className="w-3.5 h-3.5" />
                  <span>Time: {formatTimer(timerSeconds)}</span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[#7867FF] to-[#22C8E5] transition-all duration-300"
                  style={{ width: `${progressPct}%` }}
                ></div>
              </div>

              {/* Question Navigation Pill Chips */}
              <div className="flex flex-wrap gap-2">
                {questions.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrentQIdx(i)}
                    className={`w-8 h-8 rounded-lg text-xs font-bold transition-all ${
                      currentQIdx === i
                        ? 'bg-[#7867FF] text-white shadow-md shadow-[#7867FF]/40'
                        : userAnswers[i]
                        ? 'bg-[#22C8E5]/20 text-[#22C8E5] border border-[#22C8E5]/40'
                        : 'bg-white/5 text-slate-400 hover:text-white'
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}
              </div>

              {/* Current Question Body */}
              {questions[currentQIdx] && (
                <div className="p-6 rounded-2xl bg-[#0D1222] border border-white/10 space-y-5">
                  <div className="text-base font-bold text-white leading-relaxed">
                    <MathContent content={questions[currentQIdx].question} />
                  </div>

                  {/* Options List */}
                  <div className="space-y-3">
                    {questions[currentQIdx].options.map((opt, optIdx) => {
                      const isSelected = userAnswers[currentQIdx] === opt;
                      const isCorrect = questions[currentQIdx].correct === opt;

                      let optClasses = 'border-white/10 bg-[#141B2D]/60 hover:bg-[#1B2438] text-slate-200';
                      if (submitted) {
                        if (isCorrect) {
                          optClasses = 'border-emerald-500 bg-emerald-950/40 text-emerald-300 font-semibold';
                        } else if (isSelected && !isCorrect) {
                          optClasses = 'border-rose-500 bg-rose-950/40 text-rose-300';
                        }
                      } else if (isSelected) {
                        optClasses = 'border-[#7867FF] bg-[#7867FF]/15 text-white font-semibold ring-1 ring-[#7867FF]';
                      }

                      return (
                        <div
                          key={optIdx}
                          onClick={() => handleSelectOption(currentQIdx, opt)}
                          className={`p-4 rounded-xl border text-xs sm:text-sm cursor-pointer transition-all flex items-center justify-between ${optClasses}`}
                        >
                          <div className="flex items-center gap-3">
                            <span className="w-6 h-6 rounded-lg bg-white/5 flex items-center justify-center font-bold text-xs text-slate-400 shrink-0">
                              {String.fromCharCode(65 + optIdx)}
                            </span>
                            <MathContent content={opt} />
                          </div>

                          {submitted && isCorrect && (
                            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 ml-2" />
                          )}
                          {submitted && isSelected && !isCorrect && (
                            <XCircle className="w-4 h-4 text-rose-400 shrink-0 ml-2" />
                          )}
                        </div>
                      );
                    })}
                  </div>

                  {/* Explanation (Shown when submitted) */}
                  {submitted && questions[currentQIdx].explanation && (
                    <div className="p-4 rounded-xl bg-indigo-950/40 border border-[#7867FF]/30 text-xs text-slate-300 space-y-1 animate-slide-up">
                      <div className="font-bold text-[#22C8E5] flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5" /> Conceptual Explanation:
                      </div>
                      <MathContent content={questions[currentQIdx].explanation} />
                    </div>
                  )}
                </div>
              )}

              {/* Navigation Controls between questions */}
              <div className="flex justify-between items-center pt-2">
                <button
                  onClick={() => setCurrentQIdx((prev) => Math.max(prev - 1, 0))}
                  disabled={currentQIdx === 0}
                  className="btn-secondary py-2 px-4 text-xs font-semibold disabled:opacity-40"
                >
                  <ChevronLeft className="w-4 h-4" /> Previous
                </button>

                {!submitted ? (
                  currentQIdx === questions.length - 1 ? (
                    <button
                      onClick={handleSubmitQuiz}
                      className="btn-primary py-2 px-6 text-xs font-semibold"
                    >
                      <span>Submit Quiz</span>
                      <CheckCircle2 className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => setCurrentQIdx((prev) => Math.min(prev + 1, questions.length - 1))}
                      className="btn-primary py-2 px-4 text-xs font-semibold"
                    >
                      Next <ChevronRight className="w-4 h-4" />
                    </button>
                  )
                ) : (
                  <button
                    onClick={handleGenerateQuiz}
                    className="btn-secondary py-2 px-4 text-xs font-semibold"
                  >
                    <RotateCcw className="w-4 h-4" /> Retake Another Quiz
                  </button>
                )}
              </div>

              {/* Results Summary Box when submitted */}
              {submitted && (
                <div className="p-6 rounded-2xl bg-gradient-to-br from-[#7867FF]/20 to-[#22C8E5]/15 border border-[#7867FF]/40 text-center space-y-3 animate-slide-up">
                  <div className="inline-flex p-3 rounded-full bg-[#7867FF]/30 text-white shadow-lg">
                    <Award className="w-8 h-8" />
                  </div>
                  <h3 className="text-2xl font-extrabold text-white">
                    Quiz Completed!
                  </h3>
                  <div className="text-4xl font-extrabold text-gradient">
                    {quizScore} / {questions.length}
                  </div>
                  <p className="text-xs text-slate-300">
                    Accuracy Score: <strong className="text-[#22C8E5]">{Math.round((quizScore / questions.length) * 100)}%</strong> • Time: <span className="font-mono">{formatTimer(timerSeconds)}</span>
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* SUB TAB 2: CODING CHALLENGES                             */}
      {/* ========================================================= */}
      {subTab === 'coding' && (
        <div className="space-y-6">
          <div className="glass-card p-6 space-y-4">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Terminal className="w-4 h-4 text-[#22C8E5]" />
              Verified Subprocess Coding Challenges
            </h4>

            {/* Subject Selector */}
            <div className="flex flex-wrap gap-2">
              {Object.keys(challengesData).map((subj) => (
                <button
                  key={subj}
                  onClick={() => {
                    setCodingSubject(subj);
                    setSelectedChallengeIdx(0);
                    const list = challengesData[subj] || [];
                    if (list.length > 0) setUserCode(list[0].starter_code);
                    setEvalResult(null);
                  }}
                  className={`py-1.5 px-3 rounded-xl text-xs font-semibold transition-all ${
                    codingSubject === subj
                      ? 'bg-[#7867FF] text-white shadow-md'
                      : 'bg-white/5 text-slate-400 hover:text-white'
                  }`}
                >
                  {subj}
                </button>
              ))}
            </div>

            {/* Challenge List Buttons */}
            {activeChallengeList.length > 0 && (
              <div className="flex flex-wrap gap-2 pt-2 border-t border-white/5">
                {activeChallengeList.map((ch, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setSelectedChallengeIdx(idx);
                      setUserCode(ch.starter_code);
                      setEvalResult(null);
                    }}
                    className={`py-1.5 px-3 rounded-lg text-xs font-medium transition-all ${
                      selectedChallengeIdx === idx
                        ? 'bg-[#22C8E5]/20 border border-[#22C8E5]/40 text-[#22C8E5]'
                        : 'bg-white/5 text-slate-400 hover:text-white'
                    }`}
                  >
                    {ch.title}
                  </button>
                ))}
              </div>
            )}
          </div>

          {currentChallenge && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Problem Description Panel */}
              <div className="lg:col-span-5 glass-card p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-bold text-white">{currentChallenge.title}</h4>
                  <span className="domain-badge text-[10px]">
                    {currentChallenge.difficulty || 'Medium'}
                  </span>
                </div>

                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  {currentChallenge.description}
                </p>

                {currentChallenge.example && (
                  <div className="p-3.5 rounded-xl bg-[#080B16] border border-white/10 font-mono text-xs text-slate-300">
                    <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">Example:</div>
                    {currentChallenge.example}
                  </div>
                )}
              </div>

              {/* Editor & Runner Panel */}
              <div className="lg:col-span-7 glass-card p-6 space-y-4">
                <div className="flex justify-between items-center text-xs text-slate-400">
                  <span className="font-mono">solution.py</span>
                  <span>Python 3.13 Subprocess Sandbox</span>
                </div>

                <textarea
                  rows={10}
                  value={userCode}
                  onChange={(e) => setUserCode(e.target.value)}
                  className="w-full font-mono text-xs sm:text-sm bg-[#080B16] border border-white/10 rounded-xl p-3.5 text-slate-100"
                />

                <div className="flex justify-end">
                  <button
                    onClick={handleRunCodingChallenge}
                    disabled={evalLoading}
                    className="btn-primary py-2.5 px-5 text-xs font-semibold"
                  >
                    <Play className="w-4 h-4 fill-white" />
                    <span>{evalLoading ? 'Executing Test Cases...' : 'Submit & Run Test Cases'}</span>
                  </button>
                </div>

                {/* Challenge Result */}
                {evalResult && (
                  <div className="p-4 rounded-xl bg-[#0D1222] border border-white/10 space-y-2 animate-slide-up text-xs">
                    <div className="flex items-center justify-between pb-2 border-b border-white/5">
                      <span className="font-bold text-white">Test Case Evaluation</span>
                      {evalResult.all_passed ? (
                        <span className="text-emerald-400 font-bold flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> All Tests Passed!
                        </span>
                      ) : (
                        <span className="text-rose-400 font-bold flex items-center gap-1">
                          <XCircle className="w-3.5 h-3.5" /> Some Tests Failed
                        </span>
                      )}
                    </div>

                    <div className="text-slate-300 leading-relaxed">
                      {evalResult.feedback || evalResult.error}
                    </div>

                    {evalResult.execution_time_ms && (
                      <div className="text-[11px] text-slate-500 font-mono">
                        Execution Runtime: {evalResult.execution_time_ms} ms
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
