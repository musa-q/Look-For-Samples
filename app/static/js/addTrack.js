document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-track-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = {
            songName: document.querySelector('[aria-label="songName"]').value,
            artistName: document.querySelector('[aria-label="artistName"]').value,
            yearReleased: document.querySelector('[aria-label="yearReleased"]').value,
            countryReleased: document.querySelector('[aria-label="countryReleased"]').value,
            imageCoverLink: document.querySelector('[aria-label="imageCoverLink"]').value,
            youtubeLink: document.querySelector('[aria-label="youtubeLink"]').value,
            styles: [],
            genres: []
        };

        const styleInputs = document.querySelectorAll('[aria-label="styles"]');
        styleInputs.forEach(input => formData.styles.push(input.value));

        const genreInputs = document.querySelectorAll('[aria-label="genres"]');
        genreInputs.forEach(input => formData.genres.push(input.value));

        fetch('/add-track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
            .then(response => response.json())
            .then(data => console.log('Success:', data))
            .catch(error => console.error('Error:', error));
    });
});

function addInput(inputType) {
    var container;
    var inputContainerId;

    if (inputType === 'styles') {
        container = document.getElementById('styles-container');
        inputContainerId = 'styles-container';
    } else if (inputType === 'genres') {
        container = document.getElementById('genres-container');
        inputContainerId = 'genres-container';
    }

    if (container) {
        var newInput = document.createElement('div');
        newInput.className = 'input-group';
        newInput.innerHTML = `
        <input type="text" class="form-control mb-1" placeholder="${inputType.charAt(0).toUpperCase() + inputType.slice(1)}" aria-label="${inputType}" required>
    `;
        container.appendChild(newInput);
    } else {
        console.error(`Container (${inputContainerId}) not found.`);
    }
}

function removeInput(inputType) {
    var container;
    var inputContainerId;

    if (inputType === 'styles') {
        container = document.getElementById('styles-container');
        inputContainerId = 'styles-container';
    } else if (inputType === 'genres') {
        container = document.getElementById('genres-container');
        inputContainerId = 'genres-container';
    }

    if (container) {
        var inputs = container.getElementsByClassName('input-group');
        if (inputs.length > 0) {
            container.removeChild(inputs[inputs.length - 1]);
        } else {
            console.warn(`Minimum 1 ${inputType} input required.`);
        }
    } else {
        console.error(`Container (${inputContainerId}) not found.`);
    }
}