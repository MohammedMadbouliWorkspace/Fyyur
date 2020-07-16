try {
    let approveDeleteBtn = document.getElementById("approveDeleteBtn"),
        cancelDeleteBtn = document.getElementById( "cancelDeleteBtn"),
        type = approveDeleteBtn.dataset.type,
        id = approveDeleteBtn.dataset.id

    approveDeleteBtn.onclick = () => {
        fetch(`/${type}s/${id}/delete`,
            {
                method: 'DELETE'
            })
            .then((response)=>response.json())
            .then((data)=>{
                location.pathname = data.redirection
            })
    }

    cancelDeleteBtn.onclick = () => {
        location.pathname = `/profile/${type}/${id}`
    }
} catch (e) {
}