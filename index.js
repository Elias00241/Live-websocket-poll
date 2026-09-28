        // Connect to the Python WebSocket server
        const socket = new WebSocket('ws://localhost:8765');
        const statusDiv = document.getElementById('status');

        socket.onopen = () => {
            statusDiv.textContent = 'Connected to Live Server!';
            statusDiv.style.color = 'green';
        };

        socket.onclose = () => {
            statusDiv.textContent = 'Disconnected from Server.';
            statusDiv.style.color = 'red';
        };

        // Listen for data broadcast packets from the server
        socket.onmessage = (event) => {
            const voteState = JSON.parse(event.data);
            
            // Calculate total votes across all options to establish dynamic percentages
            const totalVotes = Object.values(voteState).reduce((a, b) => a + b, 0);

            // Update DOM element heights, labels, and bar widths smoothly
            for (const [language, count] of Object.entries(voteState)) {
                document.getElementById(`count-${language}`).textContent = count;
                
                // Prevent division by zero if total votes are 0
                const percentage = totalVotes > 0 ? (count / totalVotes) * 100 : 0;
                document.getElementById(`bar-${language}`).style.width = `${percentage}%`;
            }
        };

        // Function triggered when an option button is clicked
        function castVote(language) {
            if (socket.readyState === WebSocket.OPEN) {
                // Send selected option to server as a stringified JSON token
                socket.send(JSON.stringify({ vote: language }));
            }
        }