document.addEventListener('DOMContentLoaded', function () {
    var musicBox = document.querySelector('.music-box');
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