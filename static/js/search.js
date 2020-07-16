try {
    let searchBar = document.getElementById("searchBar"),
        resultsBox = document.getElementById("resultsBox");

    const searchFunction = (callback) => {

        searchBar.onkeyup = () => {

            let sendSignalTimeOut = setTimeout(() => {
                resultsBox.style.display = "block"
                callback(searchBar, resultsBox)
            }, 500)

            searchBar.onkeydown = () => {
                clearTimeout(sendSignalTimeOut)
            }

            if (!searchBar.value) {
                resultsBox.style.display = "none"
                resultsBox.innerHTML = ""
                clearTimeout(sendSignalTimeOut)
            }

        }
    }

    if (searchBar.classList.contains("search_venue")) {
        searchFunction((s, r) => {
            fetch("/venues/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "search_term": s.value
                })
            })
                .then(
                    response => response.json()
                )
                .then(
                    data => {
                        if (data.status === 'found') {
                            r.innerHTML =
                                `<h5>Number of search results for "<b>${data.search_term}</b>" is ${data.count | 0}</h5>
                          <ul class="items">
                            ${data.results.map(venue => `
                                <li>
                                    <a href="/profile/venue/${venue.id}">
                                        <i class="fas fa-music"></i>
                                        <div class="item">
                                            <h5>${venue.name}</h5>
                                        </div>
                                        <div class="item">
                                            <h5>Upcoming shows: ${venue.upcoming_shows_count}</h5>
                                            <h5>ID: ${venue.id}</h5>
                                        </div>
                                    </a>
                                </li>`).join("")}  
                        </ul>`
                        } else {
                            r.innerHTML =
                                `<h3>No results for "<b>${data.search_term}</b>"</h3>`
                        }
                    }
                )
        })
    } else if (searchBar.classList.contains("search_artist")) {
        searchFunction((s, r) => {
            fetch("/artists/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "search_term": s.value
                })
            })
                .then(
                    response => response.json()
                )
                .then(
                    data => {
                        if (data.status === 'found') {
                            r.innerHTML =
                                `<h5>Number of search results for "<b>${data.search_term}</b>" is ${data.count | 0}</h5>
                          <ul class="items">
                            ${data.results.map(artist => `
                                <li>
                                    <a href="/profile/artist/${artist.id}">
                                        <i class="fas fa-users"></i>
                                        <div class="item">
                                            <h5>${artist.name}</h5>
                                        </div>
                                        <div class="item">
                                            <h5>Upcoming shows: ${artist.upcoming_shows_count}</h5>
                                            <h5>ID: ${artist.id}</h5>
                                        </div>
                                    </a>
                                </li>`).join("")}  
                        </ul>`
                        } else {
                            r.innerHTML =
                                `<h3>No results for "<b>${data.search_term}</b>"</h3>`
                        }
                    }
                )
        })
    }
} catch (e) {
}