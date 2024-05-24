
    function updateFormAction() {
        var form = document.getElementById('signUpForm');
        var form1=document.getElementById("signInForm")
        var role = form.querySelector('select[name="role"]').value;
        var role1=form1.querySelector('select[name="role"]').value;
    //sign up form
        if (role === "admin") {
            form.action = "/admin_signup.php";
        } else if (role === "hotelier") {
            form.action = "/hotelier.php";
        } else {
            form.action = "/signup.php";
        }

        // sign in form
        if (role1 === "admin") {
            form1.action = "/admin_login.php";
        } else if (role1 === "hotelier") {
            form1.action = "/hotelier_login.php";
        } else {
            form1.action = "/login.php";
        }
    }
    
    function toggleSidebar() {
        var sidebar = document.getElementById("sidebar");
        if (sidebar.style.width === "250px") {
            sidebar.style.width = "0";
        } else {
            sidebar.style.width = "250px";
        }
    }

    function closeSidebar() {
        var sidebar = document.getElementById("sidebar");
        sidebar.style.width = "0";
    }

    function logout() {
        fetch('/logout.php', {
            method: 'POST',
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/login.html';
            } else {
                alert('Logout failed:', response.statusText);
            }
        })
        .catch(error => {
            alert('Error during logout:', error);
        });
    }

    function changePassword() {
        alert("Reset Password clicked!");
    }

    function validateEmail() {
    const email = document.getElementById("email").value;
    if (email.length === 0 || email.indexOf("@") === -1 || email.indexOf(".") === -1) {
        alert("You must enter a valid email");
        document.getElementById("email").focus();
        return false;
    }
    
}
    function validateUsername(){
        const username=docment.getElementById("username");
        if (!username || username.length <= 4){
            alert("Username must be more than 4 letters")
            document.getElementById("username").focus();
        }
    }
    function validatePhoneNum(){
        const phone_no=document.getElementById("phone_no")
        var phonePattern = /^\d{10}$/; // Regular expression for 10 digits
        return phonePattern.test(phone_no);
        if (!phone_no || !validatePhoneNumber(phone_n0)) {
            alert("Please enter a valid phone number (10 digits)");
            document.getElementById(phone_no).focus();
        }
    }   
    function showForm(formType) {
        var signUpForm = document.getElementById('signUp-form');
        var signInForm = document.getElementById('signIn-form');
        signUpForm.style.display = 'none';
        signInForm.style.display = 'none';

        if (formType === 'signUp') {
            signUpForm.style.display = 'block';
        } else if (formType === 'signIn') {
            signInForm.style.display = 'block';
        }
    }


// Validate password
function validatePassword() {
    const password = document.getElementById("passwd").value;
    if (password.length < 8) {
        alert("Password must be at least 8 characters long");
        document.getElementById("passwd").focus();
        return true;
    }
}
//function vvalidateConfirm password
    function confirmPassword(){
        const password = document.getElementById("passwd").value;
        const conf_password = document.getElementById("conf_passwd").value;

        if (password == !conf_password){
            alert("Passwords do not match")
            document.getElementById("conf_passwd").focus();
        }
    }

function validateForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("passwd").value;
    const username=docment.getElementById("username");
    const phone_no=document.getElementById("phone_no");
    const conf_password = document.getElementById("conf_passwd").value;


    if (username == "") {
        alert("Please enter username");
        document.getElementById("username").focus();
        return true;
    }
    if (email == "") {
        alert("Please enter email");
        document.getElementById("email").focus();
        return true;
    }
    if (phone_no == "") {
        alert("Please enter phone number");
        document.getElementById("phone_no").focus();
        return true;
    }
    if (password == "") {
        alert("Please enter password");
        document.getElementById("passwd").focus();
        return true;
    }
    if (conf_password == "") {
        alert("Please confirm password");
        document.getElementById("conf_passwd").focus();
        return true;
    }

    var val = true;
    val = validateEmail();
    if (val == true);
    val = validatePassword();
    if (val == true);
    val=validatePhoneNum();
    if(val == true);
    val=validateUsername();
    if(val == true);
    val=confirmPassword();
    if(val == true);
    return true;

}
function closeForm(formId) {
    var form = document.getElementById(formId);
    form.style.display = 'none';
}

function fetchHotelRecommendations() {
    var hotelFeatures = document.getElementById("hotel-features").value;
    var hotelName = document.getElementById("hotel-name").value;
    var location = document.getElementById("location").value;
    var dateInput = document.getElementById("date");
    var date = dateInput.value; // Get the selected date value

    // Format the date as "YYYY,MM,DD"
    var formattedDate = date.split("-").join(",");

    var requestData = {
        "hotel_features": hotelFeatures,
        "hotel_input": hotelName,
        "location_input": location,
        "dep_date":formattedDate
    };

    fetch("http://localhost:8000", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Initialize map
        var map = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add markers for recommended hotels
        var hotelInfoContainer = document.getElementById("hotel-info-container");
        hotelInfoContainer.innerHTML = "";

        data.recommended_hotels.forEach(hotel => {
            var lat = hotel.location.latitude;
            var lon = hotel.location.longitude;
            var hotelName = hotel.name;
            var rating = hotel.rating;
            var reviews = hotel.reviews || "No reviews available";
            var weather = hotel.weather || {};

            // Add marker to the map
            var marker = L.marker([lat, lon]).addTo(map)
                .bindPopup(`<b>${hotelName}</b><br>Rating: ${rating}`)
                .openPopup();

            // Create hotel info container
            var hotelInfo = document.createElement("div");
            hotelInfo.classList.add("hotel-info");

            hotelInfo.innerHTML = `<b>${hotelName}</b><br>Rating: ${rating}<br><br><b>Reviews:</b><br>${reviews}`;

            // Weather information
            var weatherInfo = document.createElement("div");
            weatherInfo.classList.add("weather-info");
            var weatherIcon = document.createElement("img");
            weatherIcon.src = `http://openweathermap.org/img/wn/${weather.icon}.png`;
            weatherIcon.alt = weather.description;
            weatherInfo.appendChild(weatherIcon);
            weatherInfo.innerHTML += `<span>${weather.temperature}°C, ${weather.description}</span>`;
            hotelInfo.appendChild(weatherInfo);

            // Button for viewing location on the map
            var viewLocationButton = document.createElement("button");
            viewLocationButton.innerHTML = "View Location on Map";
            viewLocationButton.onclick = function() {
                var url = `http://maps.google.com/maps?q=${lat},${lon}&name=${encodeURIComponent(hotelName)}`;
                window.open(url, '_blank');
            };
            hotelInfo.appendChild(viewLocationButton);

            // Button for Google search link
            var googleSearchButton = document.createElement("button");
            googleSearchButton.innerHTML = "Google Search";
            googleSearchButton.classList.add("google-search-button");
            googleSearchButton.onclick = function() {
                var searchUrl = `https://www.google.com/search?q=${encodeURIComponent(hotelName)}+${encodeURIComponent(hotel.country)}`;
                window.open(searchUrl, '_blank');
            };
            hotelInfo.appendChild(googleSearchButton);

            hotelInfoContainer.appendChild(hotelInfo);
        });

        // Display flight information
        var flightInfoContainer = document.getElementById("flight-info-container");
        flightInfoContainer.innerHTML = "";

        if (data.flights_info && data.flights_info.length > 0) {
            var flightInfoTitle = document.createElement("h2");
            flightInfoTitle.textContent = "Flight Information";
            flightInfoContainer.appendChild(flightInfoTitle);

            data.flights_info.forEach(flight => {
                var flightInfo = document.createElement("div");
                flightInfo.classList.add("flight-info");

                flightInfo.innerHTML = `<b>Flight from ${flight.origin} to ${flight.destination}</b><br>
                                        Departure: ${flight.departure_time}<br>
                                        Arrival: ${flight.arrival_time}<br>
                                        Duration: ${flight.duration}<br>
                                        Price: ${flight.price}`;

                flightInfoContainer.appendChild(flightInfo);
            });
        } else {
            var noFlightsInfo = document.createElement("p");
            noFlightsInfo.textContent = "No flight information available.";
            flightInfoContainer.appendChild(noFlightsInfo);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
// Function to fetch hotel recommendations
        function fetchHotelRecommendations() {
            var location = document.getElementById("location").value;

            var requestData = {
                "location_input": location
            };

            // Make a POST request to the server
            fetch("http://localhost:8000", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the hotel info container with the received data
                var hotelInfoContainer = document.getElementById("hotel-info-container");
                hotelInfoContainer.innerHTML = ""; // Clear previous content

                if (data.message) {
                    hotelInfoContainer.innerHTML = `<p>${data.message}</p>`;
                } else {
                    data.recommended_hotels.forEach(hotel => {
                        var hotelCard = document.createElement("div");
                        hotelCard.classList.add("hotel-card");

                        var hotelImage = document.createElement("img");
                        hotelImage.src = "img/bed2.png";
                        hotelImage.alt = "Hotel Image";
                        hotelCard.style.backgroundSize = "cover"; // Adjusts the size of the background image to cover the entire element
                        hotelCard.style.backgroundPosition = "center"; // Centers the background image within the element
                        hotelCard.style.width = "300px"; // Adjust as needed
                        hotelCard.style.height = "300px";

                        var hotelCardContent = document.createElement("div");
                        hotelCardContent.classList.add("hotel-card-content");

                        var hotelName = document.createElement("h3");
                        hotelName.textContent = hotel.name;

                        var hotelRating = document.createElement("p");
                        hotelRating.textContent = `Rating: ${hotel.rating}`;

                        var googleSearchLink = document.createElement("a");
                        googleSearchLink.href = hotel.google_search_link;
                        googleSearchLink.target = "_blank";
                        googleSearchLink.textContent = "Google Search";

                        hotelCardContent.appendChild(hotelName);
                        hotelCardContent.appendChild(hotelRating);
                        hotelCardContent.appendChild(googleSearchLink);

                        hotelCard.appendChild(hotelImage);
                        hotelCard.appendChild(hotelCardContent);

                        hotelInfoContainer.appendChild(hotelCard);
                    });
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        }