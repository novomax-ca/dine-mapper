window.resetFormErrors = function () {
    let el = document.forms[0].elements;
    for (let i = 0; i < el.length; i++) {
        let elem = el[i];

        if (elem.classList.contains("is-invalid")) {
            elem.classList.remove("is-invalid");
        }
        let invalidFeedback = elem.parentNode.querySelector("div.invalid-feedback");
        if (invalidFeedback) {
            invalidFeedback.remove();
        }
    }
    let invalidElements = document.querySelectorAll(".is-invalid");

    if (invalidElements.length !== 0) {
        invalidElements.forEach((el) => {
            el.classList.remove("is-invalid");
        });
    }
}

window.generateFormErrors = function (errors, node) {
    for (const prop in errors) {
        if (errors.hasOwnProperty(prop)) {
            let input2 = document.querySelectorAll("form [name$='" + prop + "']");
            if (input2.length === 0) {
                let input3 = document.querySelectorAll("form [name$='" + prop + "[]']");
                let selectedDiv = input3[0].parentElement.parentElement.parentElement;
                selectedDiv.classList.add("is-invalid");

                errors[prop].forEach((el) => {
                    let div = document.createElement("div");
                    div.className = "invalid-feedback d-block";
                    div.innerText = el;
                    selectedDiv.after(div);
                });
            } else if (input2.length === 1) {
                let input = input2[0];
                input.classList.add("is-invalid");

                errors[prop].forEach((el) => {
                    let div = document.createElement("div");
                    div.className = "invalid-feedback d-block";
                    div.innerText = el;
                    input.after(div);
                });
            }
        }
    }
}

function startBtnLoader(btn, without_loader = false) {
    let submit = document.querySelector(btn);
    submit.disabled = true;

    if (without_loader !== true) {
        let spinner = document.createElement('span');
        spinner.id = 'spinnerLoader';
        spinner.className = 'spinner-border spinner-border-sm';
        spinner.role = 'status';
        spinner.ariaHidden = 'true';
        submit.prepend(spinner);
    }
}

function endBtnLoader(btn) {
    let submit = document.querySelector(btn);
    submit.disabled = false;
    let spinner = document.querySelector('#spinnerLoader');
    if (spinner) {
        spinner.remove();
    }
}

function renderListItem(item) {
    console.log(item);
    console.log(item['fields']);
    let rating = '';
    for (let i = 1; i <= item['fields']['rating']; i++) {
        rating += '<i class="icon-star"></i>';
    }
    return '<div id="marker_'+item['pk']+'" data-location="'+item['fields']['longitude']+':'+item['fields']['latitude']+'" class="list-group-item list-group-item-action">'+
                '<div class="row align-items-center">'+
                    '<div class="col-auto">'+
                        '<img src="/media/'+item['fields']['thumbnail']+'" onerror="this.onerror=null;this.src=\'/static/images/empty_photo.gif\';" width="150" class="img-fluid" alt="Restaurant Image">'+
                    '</div>'+
                    '<div class="col">'+
                        '<div class="d-flex w-100 justify-content-between">'+
                            '<h4 class="mb-1">'+item['fields']['name']+'</h4>'+
                            '<button type="button" class="btn btn-sm btn-danger remove_marker" id="remove_marker_'+item['pk']+'">'+
                                '<i class="icon-remove"></i>'+
                            '</button>'+
                        '</div>'+
                        '<div><small>'+item['fields']['visited_at']+'</small></div>'+
                        '<p class="mb-1">'+item['fields']['review']+'</p>'+
                        '<div>'+rating+'</div>'+
                    '</div>'+
                '</div>'+
            '</div>';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

function handleRemoveMarker(markersMap) {
    let removeButtons = document.querySelectorAll('.remove_marker');

    removeButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();
            let markerId = event.currentTarget.id.split('_')[2];

            let button = event.currentTarget;
            if (button) {
                button.disabled = true;
            }

            fetch('/delete_marker/' + markerId, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => {
                if (response.ok) {
                    let marker = document.getElementById('marker_' + markerId);
                    marker.remove();

                    console.log('Marker removed successfully');
                } else {
                    console.error('Error removing marker');
                }

                if (button) {
                    button.disabled = false;
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        });
    });
}

