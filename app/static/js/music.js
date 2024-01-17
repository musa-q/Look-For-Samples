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
    console.log(currentSong);
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
            document.getElementById("reportButton").style.display = "none";
        })
        .catch(error => console.error('Error:', error));
}