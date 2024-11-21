function handleJoinGroup(event, groupType) {
    event.preventDefault();
  
    const studentName = document.getElementById(`student-name-${groupType}`).value.trim();
    const membersCountEl = document.getElementById(`members-count-${groupType}`);
    const joinMessageEl = document.getElementById('join-message');
    const currentMembers = parseInt(membersCountEl.textContent);
  
    if (!studentName) {
      joinMessageEl.textContent = "Please enter your name.";
      joinMessageEl.style.color = '#e74c3c';
      joinMessageEl.style.display = 'block';
      return;
    }
  
    if (currentMembers < 3) {
      membersCountEl.textContent = currentMembers + 1;
      joinMessageEl.textContent = `Thank you, ${studentName}. You've successfully joined Group ${groupType === 'male' ? '1' : '2'}!`;
      joinMessageEl.style.color = '#27ae60';
      joinMessageEl.style.display = 'block';
    } else {
      joinMessageEl.textContent = "Sorry, the group is full. Please try another group.";
      joinMessageEl.style.color = '#e74c3c';
      joinMessageEl.style.display = 'block';
    }
  
    document.getElementById(`student-name-${groupType}`).value = ''; // Clear input
  }
  
  document.getElementById('join-group-form-male').addEventListener('submit', (event) => {
    handleJoinGroup(event, 'male');
  });
  
  document.getElementById('join-group-form-female').addEventListener('submit', (event) => {
    handleJoinGroup(event, 'female');
  });
  
  