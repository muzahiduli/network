document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(function(container) {
        container.addEventListener('click', function(event) {
            let containerElement = event.target.parentElement.parentElement;
            let modButtonsElement = containerElement.children[1];
            let contentElement = containerElement.children[2];
            let postid = containerElement.dataset.postid
            let content = contentElement.innerHTML;
    
            contentElement.innerHTML = '';
            let text = document.createElement('textarea');
            text.value = content.trim();
            text.cols = 110;
            contentElement.append(text);
            let saveButton = '<button class="save btn btn-outline-success">Save</button>';
            modButtonsElement.insertAdjacentHTML('beforeend', saveButton);

    
            containerElement.querySelector('.save').addEventListener('click', function() {
                contentElement.innerHTML = text.value;
                modButtonsElement.children[1].remove();
    
                fetch('/', {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: text.value,
                        postid: postid
                    })
                })
            })
        })
    })

    document.querySelectorAll('.like').forEach(function(like) {
        like.addEventListener('click', function(event) {
            let containerElement = event.target.parentElement;
            let postid = containerElement.dataset.postid;
            let likesCount = containerElement.querySelector('.likes-count');

            likesCount.innerHTML = parseInt(likesCount.innerHTML) + 1;
            like.style.pointerEvents = 'none';
            containerElement.querySelector('.unlike').style.pointerEvents = 'auto';

            like.style.border = 'solid';
            like.style.borderWidth = '1px';
            containerElement.querySelector('.unlike').style.border = 'none';

            fetch('/', {
                method: 'PUT',
                body: JSON.stringify({
                    like: true,
                    postid: postid
                })
            })
        })
    })

    document.querySelectorAll('.unlike').forEach(function(unlike) {
        unlike.addEventListener('click', function(event) {
            let containerElement = event.target.parentElement;
            let postid = containerElement.dataset.postid;
            let likesCount = containerElement.querySelector('.likes-count');

            likesCount.innerHTML = parseInt(likesCount.innerHTML) - 1;
            containerElement.querySelector('.like').style.pointerEvents = 'auto';
            unlike.style.pointerEvents = 'none';

            unlike.style.border = 'solid';
            unlike.style.borderWidth = '1px';
            containerElement.querySelector('.like').style.border = 'none';

            fetch('/', {
                method: 'PUT',
                body: JSON.stringify({
                    unlike: true,
                    postid: postid
                })
            })
        })
    })
    


    function changeFollow() {
        const followButtons = document.querySelector('#followButtons')
        if (followButtons.dataset.userfollowing == "True") {
            document.querySelector('#follow').style.display = 'none';
            document.querySelector('#unfollow').style.display = 'block';
            followButtons.dataset.userfollowing = "False";
        }
        else {
            document.querySelector('#follow').style.display = 'block';
            document.querySelector('#unfollow').style.display = 'none';
            followButtons.dataset.userfollowing = "True";
        }
    }

    changeFollow();
    document.querySelector('#follow').addEventListener('click', function() {
        changeFollow();
        let profile = document.querySelector('#follow').value;
        
        fetch(`/users/${profile}/following`, {
            method: 'PUT',
            body: JSON.stringify({
                follow: true
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.querySelector('#followers').innerHTML = `${result['followers']} Followers`;
        });
    })

    document.querySelector('#unfollow').addEventListener('click', function() {
        changeFollow();
        let profile = document.querySelector('#unfollow').value;
        fetch(`/users/${profile}/following`, {
            method: 'PUT',
            body: JSON.stringify({
                follow: false
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.querySelector('#followers').innerHTML = `${result['followers']} Followers`;
        });
    })
})