function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const messagesDiv = document.getElementById('messages');
    if (messageInput.value) {
      const newMessage = document.createElement('p');
      newMessage.textContent = messageInput.value;
      messagesDiv.appendChild(newMessage);
      messageInput.value = '';
    }
  }

  function openTab(evt, tabName) {
    // Hide all tab content
    const tabContent = document.querySelectorAll(".tab-content");
    tabContent.forEach((content) => content.style.display = "none");
  
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll(".tab-btn");
    tabButtons.forEach((button) => button.classList.remove("active"));
  
    // Show the current tab content and add active class to the button
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
  }
      document.getElementById('peer-search').addEventListener('input', function () {
        });

  // Retrieve student name from sessionStorage
document.addEventListener('DOMContentLoaded', () => {
  const studentName = sessionStorage.getItem('studentName') || 'Student';
  document.getElementById('student-name').textContent = studentName;
}); 