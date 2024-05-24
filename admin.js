const forms = {
    hotelier: {
        title: 'Add Hotelier',
        action: 'add_hotelier.php',
        fields: `
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Add Hotelier">
        `
    },
    hotelierUpdate: {
        title: 'Update Hotelier',
        action: 'update_hotelier.php',
        fields: `
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="New Password">
            <input type="submit" value="Update Hotelier">
        `
    },
    hotelierDelete: {
        title: 'Delete Hotelier',
        action: 'delete_hotelier.php',
        fields: `
            <input type="email" name="email" placeholder="Email" required>
            <input type="submit" value="Delete Hotelier">
        `
    },
    hotel: {
        title: 'Add Hotel',
        action: 'add_hotel.php',
        fields: `
            <input type="text" name="hotelName" placeholder="Hotel Name" required>
            <input type="text" name="location" placeholder="Location" required>
            <input type="text" name="description" placeholder="Description">
            <input type="submit" value="Add Hotel">
        `
    },
    hotelUpdate: {
        title: 'Update Hotel',
        action: 'update_hotel.php',
        fields: `
            <input type="text" name="hotelName" placeholder="Hotel Name" required>
            <input type="text" name="location" placeholder="Location" required>
            <input type="text" name="description" placeholder="New Description">
            <input type="submit" value="Update Hotel">
        `
    },
    hotelDelete: {
        title: 'Delete Hotel',
        action: 'delete_hotel.php',
        fields: `
            <input type="text" name="hotelName" placeholder="Hotel Name" required>
            <input type="submit" value="Delete Hotel">
        `
    },
    admin: {
        title: 'Add Admin',
        action: 'add_admin.php',
        fields: `
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Add Admin">
        `
    },
    adminUpdate: {
        title: 'Update Admin',
        action: 'update_admin.php',
        fields: `
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="New Password">
            <input type="submit" value="Update Admin">
        `
    },
    adminDelete: {
        title: 'Delete Admin',
        action: 'delete_admin.php',
        fields: `
            <input type="email" name="email" placeholder="Email" required>
            <input type="submit" value="Delete Admin">
        `
    }
};

function showForm(type) {
    const formContainer = document.getElementById('formContainer');
    const adminForm = document.getElementById('adminForm');
    
    if (forms[type]) {
        const form = forms[type];
        adminForm.innerHTML = '<h2>${form.title}</h2>${form.fields}';
        adminForm.action = form.action;
        formContainer.style.display = 'flex';
    } else {
        adminForm.innerHTML = '<h2>Error: Invalid form type</h2>';
        formContainer.style.display = 'flex';
    }
}

function hideForm() {
    document.getElementById('formContainer').style.display = 'none';
}

function viewData(type) {
    const viewTableContainer = document.getElementById('viewTableContainer');
    fetch('admin_view.php?type=${type}')
        .then(response => response.text())
        .then(data => {
            viewTableContainer.innerHTML = data;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            viewTableContainer.innerHTML = '<p>Error loading data. Please try again later.</p>';
        });
}