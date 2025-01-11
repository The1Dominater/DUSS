/** Navigation Buttons and Actions **
 * Handles updating pickup date and return date if checkboxes are marked
 */
// Get all div elements with class 'form-group'
const form = document.getElementById("reservation_form")
let formGroupDivs = document.querySelectorAll('div.form-group');
// Count the number of elements
let num_parts = formGroupDivs.length;
let part_index = 1;
var current_part = document.getElementById(`part_${part_index}`);

// Changes display to show next part of the form
function goForward() {
    if (checkRequiredInputs(current_part) && (part_index < num_parts)) {
        // Hide the current part
        current_part.style.display = 'none';
        // Display the next part
        part_index++;
        current_part = document.getElementById(`part_${part_index}`);
        current_part.style.display = 'block';
    }
    // If we are navigating to the final part gather and display view details
    if (part_index >= num_parts) {
        fillReviewDetails();
    }
}
// Changes display to show previous part of the form
function goBack() {
    if (part_index > 1) {
        // Hide the current part
        current_part.style.display = 'none';
        // Display the next part
        part_index--;
        current_part = document.getElementById(`part_${part_index}`);
        current_part.style.display = 'block';
    }
} 
// Checks to make sure all the elements are filled before changine the part
function checkRequiredInputs(current_part) {
    current_fields = current_part.querySelectorAll('input[required], select[required]')

    let isValid = true;

    current_fields.forEach(field => {
        if (field.checkValidity()) {
            // Remove highlight if valid
            field.classList.remove('error-field');
        } else {
            console.log('Field invalid: ' + field.id);
            // If it is the first error indicate what is wrong
            if (isValid) {
                field.reportValidity();
            }
            
            // Highlight invalid input in red
            field.classList.add('error-field');  
            isValid = false;
        }
    });

    return isValid;
}

/** Guest Management Functions **
 * Handles updating guest names and removing them
 */

/** Pickup and Return Details **
 * Handles updating pickup date and return date if checkboxes are marked
 */
// Get the pickup date inputs
const pickupSameDay = document.getElementById('pickup_same_day');
const plPickupDate = document.getElementById('pickup_date_0');
var isPickupSameDay = true;
// Get the return date inputs
const returnSameDay = document.getElementById('return_same_day');
const plReturnDate = document.getElementById('rental_days_0');
var isReturnSameDay = true;

// Toggle display of pickup and return checkboxes
function displayCheckboxes() {
    const checkboxes = document.getElementById("p_and_r_checkboxes")

    // If it's the first guest make the group checkboxes visible
    if (guestCount > 1) {
        const checkboxes = document.getElementById("p_and_r_checkboxes")
        checkboxes.style.display = "block";
    }
    else {
        checkboxes.style.display = "none";
    }
}
// Toggle pickup dates for entire party based on checkbox
function togglePickUpDate() {
    isPickupSameDay = !isPickupSameDay;

    for (let i = 1; i < guestCount; i++) {
        const guestPickUpDate = document.getElementById(`pickup_date_${i}`);
        guestPickUpDate.disabled = isPickupSameDay;
        
    }
    // If everyone is picking up on the same day make sure to update them
    // to match party leader's pick up date changes
    updateAllPickups();
}
// Toggle return dates for entire party based on checkbox
function toggleReturnDate() {
    isReturnSameDay = !isReturnSameDay;

    for (let i = 1; i < guestCount; i++) {
        const guestReturnDate = document.getElementById(`rental_days_${i}`);
        guestReturnDate.disabled = isReturnSameDay;
    }

    // If everyone is picking up on the same day make sure to update them
    // to match party leader's pick up date changes
    updateAllReturns();
}
// Matches every pickup date to pl's return pickup date
function updateAllPickups() {
    if (isPickupSameDay && (guestCount > 1)) {
        for (let i = 1; i < guestCount; i++) {
            var guestPickUpDate = document.getElementById(`pickup_date_${i}`);
            guestPickUpDate.value = plPickupDate.value;
        }
    }
}
// Matches every return date to pl's return date
function updateAllReturns() {
    if (isReturnSameDay && (guestCount > 1)) {
        for (let i = 1; i < guestCount; i++) {
            var guestReturnDate = document.getElementById(`rental_days_${i}`);
            guestReturnDate.value = plReturnDate.value;
        }
    }
}

// Add event listeners
plReturnDate.addEventListener('change', updateAllReturns);
plPickupDate.addEventListener('change', updateAllPickups);

/** Review Details Section **
 * Operates the final review part of the form
 */
// Fills in the review details based on the gathered inputs
function fillReviewDetails() {
    for (let i = 0; i < guestCount; i++) {
        var birthdayInput = document.getElementById(`birthday_${i}`);
        var equipmentInput = document.getElementById(`eq_type_${i}`);
        var note = document.getElementById(`note_${i}`);

        document.getElementById(`review_birthday_${i}`).innerHTML = birthdayInput.value;
        document.getElementById(`review_eq_type_${i}`).innerHTML = equipmentInput.options[equipmentInput.selectedIndex].text;

        // If it is the party leader display the telephone number
        if (i == 0) {
            document.getElementById(`review_telephone`).innerHTML = document.getElementById(`telephone`).value;
        }

        // if (equipmentInput == 'ski') {
        //     document.getElementById(`pk_type_${i}`);
        //     document.getElementById(`sk_height_${i}`);
        //     document.getElementById(`weight_${i}`);
        //     document.getElementById(`skier_type_${i}`);
        // }
        // else if (guestEquipmentType.value == 'snowboard') {
        //     document.getElementById(`pk_type_${i}`);
        //     document.getElementById(`sn_height_${i}`);
        //     document.getElementById(`riding_style_${i}`);
        //     document.getElementById(`l_offset_${i}`);
        //     document.getElementById(`r_offset_${i}`);
        // }
        document.getElementById(`review_pickup_date_${i}`).innerHTML = document.getElementById(`pickup_date_${i}`).value;
        document.getElementById(`review_rental_days_${i}`).innerHTML = document.getElementById(`rental_days_${i}`).value;

        // If notes is empty put in a placeholder
        if (note.value.trim() === "") {
            note.value = "None";
        }
        document.getElementById(`review_note_${i}`).innerHTML = note.value;
    }
}
// Toggles the display of the review details
function toggleReviewDetails(element) {
    element.classList.toggle("expanded");
}