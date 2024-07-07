function submitComplaint(event) {
    event.preventDefault()

    const department = document.getElementById('department').value
    const description = document.getElementById('description').value.toLowerCase()
    let valid = true;
    let message = ''

    if (department === 'BBMP' && !(description.includes('road') || description.includes('waste') || description.includes('health') || description.includes('lighting'))) {
        valid = false
        message = 'Please describe a road, waste management, health, or street lighting issue for BBMP.'
    } else if (department === 'BESCOM' && !description.includes('electric')) {
        valid = false
        message = 'Please describe an electricity issue for BESCOM.'
    } else if (department === 'BWSSB' && !(description.includes('water') || description.includes('sewage'))) {
        valid = false
        message = 'Please describe a water or sewerage issue for BWSSB.'
    } else if (department === 'BMTC' && !(description.includes('bus') || description.includes('transport'))) {
        valid = false
        message = 'Please describe a bus transport issue for BMTC.'
    }
    if (!valid) {
        alert(message)
    } else {
        document.getElementById('complaintLodgingWindow').classList.add('fade-out')
        setTimeout(() => {
            document.getElementById('complaintLodgingWindow').style.display = 'none'
            document.getElementById('complaintConfirmationWindow').style.display = 'block'
            document.getElementById('complaintConfirmationWindow').classList.remove('fade-out')
            document.getElementById('complaintConfirmationWindow').classList.add('fade-in')
        }, 500)
        document.getElementById('statusMessage').style.display = 'block'
    }
}
function navigateToStatus() {
    document.getElementById('complaintConfirmationWindow').classList.add('fade-out')
    setTimeout(() => {
        document.getElementById('complaintConfirmationWindow').style.display = 'none'
        document.getElementById('complaintStatusWindow').style.display = 'block'
        document.getElementById('complaintStatusWindow').classList.remove('fade-out')
        document.getElementById('complaintStatusWindow').classList.add('fade-in')

        document.getElementById('statusMessage').style.display = 'block'
    }, 500)
}
function checkStatus() {
    let status = document.getElementById('complaintStatus').innerText
    if (status === 'Completed') {
        document.getElementById('complaintStatusWindow').classList.add('fade-out')
        setTimeout(() => {
            document.getElementById('complaintStatusWindow').style.display = 'none'
            document.getElementById('feedbackForm').style.display = 'block'
            document.getElementById('feedbackForm').classList.remove('fade-out')
            document.getElementById('feedbackForm').classList.add('fade-in')
        }, 500)
    } else {
        alert('Complaint is not yet completed.')
    }
}
function submitFeedback() {
    alert('Feedback submitted. Thank you!')
    // Reset and hide feedback form
    document.getElementById('feedback').reset()
    document.getElementById('feedbackForm').classList.add('fade-out')
    setTimeout(() => {
        document.getElementById('feedbackForm').style.display = 'none'
        document.getElementById('complaintLodgingWindow').style.display = 'block'
        document.getElementById('complaintLodgingWindow').classList.remove('fade-out')
        document.getElementById('complaintLodgingWindow').classList.add('fade-in')
    }, 500)
}
function navigateToLodging() {
    document.getElementById('complaintConfirmationWindow').classList.add('fade-out')
    document.getElementById('complaintStatusWindow').classList.add('fade-out')
    document.getElementById('feedbackForm').classList.add('fade-out')

    setTimeout(() => {
        document.getElementById('complaintConfirmationWindow').style.display = 'none'
        document.getElementById('complaintStatusWindow').style.display = 'none'
        document.getElementById('feedbackForm').style.display = 'none'

        document.getElementById('complaintForm').reset()
        document.getElementById('statusMessage').style.display = 'none'

        document.getElementById('complaintLodgingWindow').style.display = 'block'
        document.getElementById('complaintLodgingWindow').classList.remove('fade-out')
        document.getElementById('complaintLodgingWindow').classList.add('fade-in')
    }, 500)
}
function showFeedbackMessage() {
    document.getElementById('feedbackMessage').style.display = 'block'
    document.getElementById('newComplaintButton').style.display = 'block'
}