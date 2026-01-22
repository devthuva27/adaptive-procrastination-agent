import React, { useState } from 'react';
import TaskForm from './components/TaskForm';

function App() {
  const [suggestion, setSuggestion] = useState(null);
  const [taskType, setTaskType] = useState('general');
  const [loading, setLoading] = useState(false);

  const handleFeedback = async (feedbackType) => {
    if (!suggestion || suggestion.completed) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          feedback: feedbackType,
          current_step: suggestion.original_subtask || suggestion.subtask,
          all_steps: suggestion.all_steps || [],
          current_index: suggestion.current_index || 0,
          original_task: suggestion.original_task || '',
          task_type: taskType
        }),
      });
      const data = await response.json();
      setSuggestion(data);
    } catch (error) {
      console.error("Error sending feedback:", error);
      setSuggestion({ error: "Failed to process feedback. Is the backend running?" });
    } finally {
      setLoading(false);
    }
  };

  const handleNewSuggestion = (data, type) => {
    setSuggestion(data);
    setTaskType(type || 'general');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center justify-center">
      <div className="w-full max-w-5xl space-y-8">
        <div className="text-center animate-fade-in max-w-2xl mx-auto">
          <h2 className="text-5xl font-black text-gray-900 tracking-tighter sm:text-6xl mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
            Momentum
          </h2>
          <p className="text-xl text-gray-600 font-medium">Break it down. Get it done.</p>
        </div>

        <TaskForm onSuggestion={handleNewSuggestion} />

        {suggestion && (
          <div className={`mt-8 p-8 bg-white rounded-xl shadow-xl border-l-4 animate-fade-in w-full ${suggestion.error ? 'border-red-500' :
              suggestion.completed ? 'border-green-500' :
                'border-emerald-500'
            }`}>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              {suggestion.error ? 'Error' :
                suggestion.completed ? '🎉 Task Complete!' :
                  'Here is your step:'}
            </h3>
            <p className={`text-xl font-medium leading-relaxed ${suggestion.error ? 'text-red-600' :
                suggestion.completed ? 'text-green-600' :
                  'text-indigo-700'
              }`}>
              {suggestion.error ? suggestion.error :
                suggestion.completed ? suggestion.subtask :
                  `"${suggestion.subtask}"`}
            </p>

            {suggestion.broken_down && (
              <p className="text-sm text-amber-600 mt-2 italic">
                ✨ Broken down into an even smaller step for you!
              </p>
            )}

            {suggestion.size && !suggestion.error && !suggestion.completed && (
              <>
                <div className="mt-4 flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${suggestion.size === 'small' ? 'bg-blue-100 text-blue-800' : 'bg-orange-100 text-orange-800'
                    }`}>
                    {suggestion.size} Effort
                  </span>
                  <span className="text-xs text-gray-400">Powered by AI</span>
                </div>

                {/* Feedback Buttons */}
                <div className="mt-6 flex gap-4">
                  <button
                    onClick={() => handleFeedback('done')}
                    disabled={loading}
                    className="flex-1 py-3 px-6 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold rounded-lg shadow-md hover:from-green-600 hover:to-emerald-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Processing...' : '✓ Done! Next Step'}
                  </button>
                  <button
                    onClick={() => handleFeedback('too_hard')}
                    disabled={loading}
                    className="flex-1 py-3 px-6 bg-gradient-to-r from-amber-500 to-orange-600 text-white font-semibold rounded-lg shadow-md hover:from-amber-600 hover:to-orange-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Processing...' : '🔨 Too Hard, Break It Down'}
                  </button>
                </div>
              </>
            )}

            {suggestion.completed && (
              <div className="mt-6">
                <button
                  onClick={() => setSuggestion(null)}
                  className="w-full py-3 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:from-indigo-700 hover:to-purple-700 transition-all duration-300"
                >
                  🚀 Start New Task
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
