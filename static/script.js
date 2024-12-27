document.addEventListener('DOMContentLoaded', function() {
    const goalForm = document.getElementById('goalForm');
    const workoutPlan = document.getElementById('workoutPlan');
    const planContent = document.getElementById('planContent');

    // Load existing plan if available
    fetch('/get_plan')
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                displayWorkoutPlan(data);
            }
        });

    goalForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Collect form data
        const goals = Array.from(document.getElementById('goals').selectedOptions)
            .map(option => option.value);
        
        const exercises = Array.from(document.querySelectorAll('input[name="exercise_type"]:checked'))
            .map(checkbox => checkbox.value);
        
        const availability = Array.from(document.querySelectorAll('input[name="availability"]:checked'))
            .map(checkbox => checkbox.value);

        // Validate form
        if (goals.length === 0 || exercises.length === 0 || availability.length === 0) {
            alert('Please fill in all required fields');
            return;
        }

        // Send data to server
        fetch('/save_goals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                goals: goals,
                exercises: exercises,
                availability: availability
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayWorkoutPlan(data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving your plan');
        });
    });

    function displayWorkoutPlan(data) {
        workoutPlan.classList.remove('hidden');
        planContent.innerHTML = '';

        // Create weekly plan display
        const plan = data.plan;
        Object.entries(plan).forEach(([day, workout]) => {
            const dayCard = document.createElement('div');
            dayCard.className = 'workout-card bg-gray-50 p-4 rounded-lg shadow-sm mb-4';
            
            let exerciseHtml = '';
            workout.exercises.forEach(exercise => {
                exerciseHtml += `
                    <div class="mb-3 border-l-4 border-red-400 pl-3">
                        <h4 class="font-medium text-gray-800">${exercise.name}</h4>
                        <p class="text-sm text-gray-600">
                            <span class="font-medium">Variation:</span> ${exercise.variation}<br>
                            <span class="font-medium">${exercise.rep_range ? 'Reps:' : 'Duration:'}</span> ${exercise.rep_range || exercise.duration}<br>
                            <span class="font-medium">Sets:</span> ${workout.sets}
                        </p>
                    </div>
                `;
            });

            dayCard.innerHTML = `
                <div class="flex items-center justify-between mb-3">
                    <h3 class="text-lg font-semibold text-red-600">${day}</h3>
                    <span class="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                        ${workout.intensity} Intensity
                    </span>
                </div>
                <div class="mb-3">
                    <p class="text-sm text-gray-600">
                        <span class="font-medium">Rest between sets:</span> ${workout.rest_between_sets}
                    </p>
                </div>
                <div class="exercise-list">
                    ${exerciseHtml}
                </div>
                <div class="mt-3 pt-3 border-t border-gray-200">
                    <p class="text-sm text-gray-600 italic">${workout.notes}</p>
                </div>
            `;
            
            planContent.appendChild(dayCard);
        });

        // Scroll to plan
        workoutPlan.scrollIntoView({ behavior: 'smooth' });
    }
});
