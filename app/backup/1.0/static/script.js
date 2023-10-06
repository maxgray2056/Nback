$(document).ready(function() {
    var itemButton = $('#item-button');
    var scoreDisplay = $('#score');

    // Get a new item from the server
    function getNewItem() {
        $.getJSON('/get_item', function(data) {
            itemButton.text(data.item);
            itemButton.prop('disabled', false);
        });
    }

    // Check if the clicked item matches the item N steps back
    function checkMatch(clickedItem) {
        $.getJSON('/check_match/' + clickedItem, function(data) {
            scoreDisplay.text(data.score);
            itemButton.prop('disabled', true);
            setTimeout(getNewItem, 1000);
        });
    }

    // Attach click event listener to item button
    itemButton.on('click', function() {
        checkMatch(itemButton.text());
    });

    // Start the game
    getNewItem();
});
