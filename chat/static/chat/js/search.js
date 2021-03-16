//Default FriendList
let DefaultFriendList = document.getElementById("friendList").getElementsByTagName("a");
let modalTag = document.getElementById("displayFriendList");

//Adding Friend List to Modal for Lower Viewport
let fragment = new DocumentFragment();
for (i = 0; i < DefaultFriendList.length; i++) {
    friend = DefaultFriendList[i].getAttribute("data-friendname");
        let div = document.createElement('div');
        div.innerHTML=`<a href="${window.location.pathname}?recipient=${friend}" class="list-group-item border-0 list-group-item-action ml-1 ${friend == recipient ? 'bg-dark':''} friend-list" data-friendname="${friend}">
                            <div class="d-flex align-items-start">${person}
                                <div class="1 ml-3">${friend}  <!-- Buggy -->
                                    <div class="small text-muted">Online</div>
                                </div>
                            </div>
                        </a>`
        fragment.appendChild(div);
        modalTag.appendChild(fragment);
}

//Search for a Friend
function searchFriend(element) {
    // Double Binding of inputs
    document.getElementById("Search").value = element.value;
    document.getElementById("SearchModal").value = element.value;
    let search = element.value;

    //Filter condition
    let filter = search.toUpperCase();

    //Taking out Children from the Parent node.
    modalTagChildren = modalTag.getElementsByTagName("a");

    //The good stuff (Filtering)
    for (i = 0; i < DefaultFriendList.length; i++) {
        friend = DefaultFriendList[i].getAttribute("data-friendname");
        if (friend.toUpperCase().includes(filter)) {
            modalTagChildren[i].style.display = "";
            DefaultFriendList[i].style.display = "";
        } else {
            modalTagChildren[i].style.display = "none";
            DefaultFriendList[i].style.display = "none";
        }
    }
}


