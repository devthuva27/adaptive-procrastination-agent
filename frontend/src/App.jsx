import React, { useState } from 'react';
import TaskForm from './components/TaskForm';

function App() {
  const [suggestion, setSuggestion] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8 flex flex-col items-center justify-center">
      <div className="w-full max-w-5xl space-y-8">
        <div className="text-center animate-fade-in max-w-2xl mx-auto">
          <h2 className="text-5xl font-black text-gray-900 tracking-tighter sm:text-6xl mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
            Momentum
          </h2>
          <p className="text-xl text-gray-600 font-medium">Break it down. Get it done.</p>
        </div>

        <TaskForm onSuggestion={setSuggestion} />

        {suggestion && (
          <div className={`mt-8 p-8 bg-white rounded-xl shadow-xl border-l-4 animate-fade-in w-full ${suggestion.error ? 'border-red-500' : 'border-emerald-500'}`}>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              {suggestion.error ? 'Error' : 'Here is your step:'}
            </h3>
            <p className={`text-xl font-medium leading-relaxed ${suggestion.error ? 'text-red-600' : 'text-indigo-700'}`}>
              {suggestion.error ? suggestion.error : `"${suggestion.subtask}"`}
            </p>
            {suggestion.size && !suggestion.error && (
              <div className="mt-4 flex items-center justify-between">
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${suggestion.size === 'small' ? 'bg-blue-100 text-blue-800' : 'bg-orange-100 text-orange-800'
                  }`}>
                  {suggestion.size} Effort
                </span>
                <span className="text-xs text-gray-400">Powered by AI</span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
