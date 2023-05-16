function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2)
        return parts.pop().split(';').shift();
}

function saveChanges(id){
    const textareaValue = document.getElementById(`textarea_${id}`).value;
    const content= document.getElementById(`postBody_${id}`);
    const modal = document.getElementById(`modal_edit_${id}`);
    console.log(modal);
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"content-type": "application/json", "X-CSRFToken":getCookie("csrftoken")},
        body: JSON.stringify({
            content: textareaValue
        })
    })
    .then(response => response.json())
    .then(result => {

        content.innerHTML = result.data;

        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

        for(let i=0; i<modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);
          }
    })
}
