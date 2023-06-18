

function checkRadio() {
    var publicid = document.getElementById("publicid");
    var friends_onlyid = document.getElementById("friends_onlyid");
    var only_meid = document.getElementById("only_meid");

    var public_container = document.getElementById("public_posts_container")
    var friends_only_container = document.getElementById("friends_only_post_container")
    var only_me_container = document.getElementById("only_me_posts_container")

    if (publicid.checked) {
        console.log("public")
        only_me_container.classList.add('d-none');
        friends_only_container.classList.add('d-none');
        public_container.classList.remove('d-none');

    } else if (friends_onlyid.checked) {
        console.log("friends")
        only_me_container.classList.add('d-none');
        friends_only_container.classList.remove('d-none');
        public_container.classList.add('d-none');

    } else {
        only_me_container.classList.remove('d-none');
        friends_only_container.classList.add('d-none');
        public_container.classList.add('d-none');
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Add smooth scrolling behavior
    });

    const input = document.getElementsByClassName('input_x')[0];
    input.focus();
}


// window.onload = function() {
//   // your script goes here
//     console.log('Page loaded');
//     postcontent = "edit content"
//     edit_form_content = document.getElementById('edit_form_content')
//     console.log(edit_form_content);
//     edit_form_content.value = postcontent
// };

postcontent = "xxxxxxxxxxxxxx"
edit_form_content = document.getElementById('edit_form_content')
// console.log(postcontent);
edit_form_content.innertext = postcontent



function openEditForm(postcontent) {
    console.log("hi")

    form = document.getElementById('edit_post_container_id');
    form.classList.remove('edit_post_container');
    form.classList.add("edit_post_container2")

    edit_form_content = document.getElementById('edit_form_content')
    console.log(postcontent);
    edit_form_content.innertext = postcontent


    // fetch('/edit_post/' + postId)
    //     .then(response => response.json())
    //     .then(data => {
    //     // Populate form fields with data
    //     document.getElementById('title').value = data.title;
    //     document.getElementById('content').value = data.content;
    //     // Show edit form
    //     document.getElementById('edit-form').style.display = 'block';
    // });
}

function closetab(){
    form = document.getElementById('edit_post_container_id');
    form.classList.remove("edit_post_container2")
    form.classList.add('edit_post_container');
    
}


  // Get the value of the variable from the query string
const url =  window.location.href;
const parts = url.split('/');
const post_id = parts[parts.length - 1];

// const urlParams = new URLSearchParams(queryString);
// const variableValue = urlParams.get('variable_name');

window.onload = function() {
    console.log(post_id)
}
  // Do something with the variable value
