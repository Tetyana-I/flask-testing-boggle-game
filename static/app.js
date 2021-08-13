// time for a player has for a guess, restart after each successful guess
const timeToGuess = 60;
// time left from the last successful guess till the end of the game
let timeLeft = timeToGuess;

showTimer();

// set of valid words that player already quessed
const wordsChecked = new Set();

// current score
let score = 0;
const $score = $('.score')

// shows time left on HTML game-page 
function showTimer(){
   $(".timer").text(timeLeft);
}

// run timer, shows on HTML, stops after finishing timeToGuess and checks for a new record
async function runTimer() {
    timeLeft--;
    showTimer();
    if (timeLeft === 0) {
        clearInterval(timer);
        await gameOver();
    }
}
let timer = setInterval(runTimer,1000);

// shows current score on HTML
function showScore(score){
    $score.empty().text(score)
}

// swows feedback messages for a player
function showMessage(msg) {
    $(".feedback-messages").empty().text(msg);
}
 
// guess-handler that asks server to check for validity and return a feedback-message 
$('#guess').on('submit', async function handleSubmit(evt) {
    evt.preventDefault();
    const $guess = $("#guess-input");
    let guess = $guess.val();
    if (!guess)
        return;
    
    if (wordsChecked.has(guess)) {
        showMessage(`Already found ${guess}`);
        return;
        }
    
    // check server for validity:
    const res = await axios.get("/guess", {params: {word: guess} });
    if (res.data.result === "not-word") {
        showMessage(`${guess} is not a valid English word`);
        }
    else
    {
        if (res.data.result === "not-on-board") {
            showMessage(`${guess} is not a valid word on this board`);
            } 
        else {
            wordsChecked.add(guess);
            showMessage(`Added: ${guess}`);
            score += guess.length;
            showScore(score);
            $(".words").append($("<li>", {text: guess}));
            timeLeft = timeToGuess;
            }
        } 
    $guess.val("").focus();
});

// checks if a new record was set and shows an appropriate message
async function gameOver() {
    $("#guess").hide();
    console.log("score",score);
    const res = await axios.post("/game-over", {score: score});
    console.log("res",res)
    if (res.data.newRecord) {
        showMessage(`Congratulations! You set a new record: ${score}`);
    } else {
      showMessage(`Final score: ${score}`);
    }
  }
