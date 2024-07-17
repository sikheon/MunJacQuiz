document.addEventListener("DOMContentLoaded", function () {
    function validateForm(event) {
        var inputs = document.querySelectorAll('.form-group input');
        var isValid = true;

        inputs.forEach(function (input) {
            var errorMessage = input.nextElementSibling;
            if (input.value.trim() === '') {
                input.classList.add('error');
                errorMessage.textContent = '이 필드는 필수입니다.';
                errorMessage.style.display = 'block';
                isValid = false;
            } else {
                input.classList.remove('error');
                errorMessage.style.display = 'none';
            }
        });

        if (!isValid) {
            event.preventDefault();
        }

        return isValid;
    }

    var form = document.getElementById('signup-form');
    form.addEventListener('submit', validateForm);

    var nicknameInput = document.getElementById('nickname');
    var nicknameError = document.getElementById('nickname-error');

    nicknameInput.addEventListener('blur', function () {
        var nickname = this.value.trim();
        if (nickname === '') {
            nicknameError.textContent = '닉네임을 입력해주세요.';
            nicknameError.style.display = 'block';
            return;
        }

        fetch('/check_nickname', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name=csrf_token]').value
            },
            body: JSON.stringify({ nickname: nickname })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('서버에서 오류가 발생했습니다.');
            }
            return response.json();
        })
        .then(data => {
            if (!data.available) {
                nicknameError.textContent = '이미 사용 중인 닉네임입니다.';
                nicknameError.style.display = 'block';
            } else {
                nicknameError.textContent = '사용 가능한 닉네임입니다.';
                nicknameError.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            nicknameError.textContent = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
            nicknameError.style.display = 'block';
        });
    });
});