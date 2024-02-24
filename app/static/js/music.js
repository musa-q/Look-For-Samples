document.addEventListener('DOMContentLoaded', function () {
    var musicBox = document.querySelector('.box');
    var hammer = new Hammer(musicBox);

    hammer.on('swiperight', function () {
        handleSwipe('LIKE');
    });

    hammer.on('swipeleft', function () {
        handleSwipe('DISLIKE');
    });

    function handleSwipe(action) {
        const duration = 200;

        if (action == 'LIKE') {
            musicBox.classList.add('slide-right');
            setTimeout(function () {
                musicBox.classList.remove('slide-right');
                submitForm(action);
            }, duration);
        }
        if (action == 'DISLIKE') {
            musicBox.classList.add('slide-left');
            setTimeout(function () {
                musicBox.classList.remove('slide-left');
                submitForm(action);
            }, duration);
        }
    }

    function submitForm(action) {
        var hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'decide_song_button';
        hiddenInput.value = action;

        var form = document.querySelector('form');
        form.appendChild(hiddenInput);

        form.submit();
    }
});

function reportTrack(currentSong) {
    var jsonString = JSON.stringify(currentSong);

    fetch('/report-track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonString,
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById("confirmationMessage").innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function copyLink(link) {
    var copyButton = document.getElementById("copyLinkButton");
    navigator.clipboard.writeText(link)
        .then(() => {
            copyButton.textContent = "Copied";
            setTimeout(function () {
                copyButton.textContent = "Copy text";
            }, 4000);
        })
        .catch((error) => {
            console.error('Failed to copy: ', error);
        });
}

function submitFeedbackForm() {
    const toastLiveExample = document.getElementById('liveToast');
    const selectedOption = document.querySelector('input[name="feedback-faces"]:checked');
    const optionValue = selectedOption ? selectedOption.value : null;
    const comment = document.getElementById('feedback-comment').value;
    var jsonString = JSON.stringify({ 'face': optionValue, 'feedback': comment });

    fetch('/add-feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonString,
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
            document.getElementById("toast-body-text").innerHTML = data.message;
            toastBootstrap.show()
        })
        .catch(error => console.error('Error:', error));
}