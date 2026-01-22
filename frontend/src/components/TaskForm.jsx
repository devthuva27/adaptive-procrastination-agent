import React, { useState } from 'react';

const TaskForm = ({ onSuggestion }) => {
    const [task, setTask] = useState('');
    const [type, setType] = useState('general');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!task.trim()) return;

        setLoading(true);
        if (onSuggestion) onSuggestion(null);

        try {
            const response = await fetch('http://localhost:5000/api/suggest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_text: task, task_type: type }),
            });
            const data = await response.json();
            onSuggestion(data);
        } catch (error) {
            console.error("Error fetching suggestion:", error);
            onSuggestion({ subtask: "Error connecting to server. Is the backend running?", size: "error" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-md mx-auto bg-white rounded-xl shadow-lg p-8 transform transition-all hover:scale-[1.01] duration-300">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Defeat Procrastination</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">What do you need to do?</label>
                    <input
                        type="text"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-colors"
                        placeholder="e.g. Write report, Clean room..."
                        value={task}
                        onChange={(e) => setTask(e.target.value)}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                    <select
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                        value={type}
                        onChange={(e) => setType(e.target.value)}
                    >
                        <option value="general">General</option>
                        <option value="work">Work</option>
                        <option value="study">Study</option>
                        <option value="chores">Chores</option>
                    </select>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-3 rounded-lg text-white font-semibold shadow-md transition-all duration-300 ${loading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 hover:shadow-lg'
                        }`}
                >
                    {loading ? 'Thinking...' : 'Get Micro-Task'}
                </button>
            </form>
        </div>
    );
};

export default TaskForm;
