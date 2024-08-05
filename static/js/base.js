// <!-- script to show/hide paylater & All messages section -->

$(document).ready(function () {

    $("#replylater").click(function () {
        $(".chatstrip").hide();
        $("#searchbox").hide();
        $("#defaultmessage").show();

        $("#replylater").removeClass("btn-secondary").addClass("btn-primary");
        $("#allmessages").removeClass("btn-primary").addClass("btn-secondary");

    });

    $("#allmessages").click(function () {
        $(".chatstrip").show();
        $("#searchbox").show();
        $("#defaultmessage").hide();

        $("#allmessages").removeClass("btn-secondary").addClass("btn-primary");
        $("#replylater").removeClass("btn-primary").addClass("btn-secondary");
    });

});
// <!-- script to show/hide paylater & All messages section -->

// <!-- manage tab content data -->
    function opentaskmanagertabs(evt, navtaskmanagertabName) {
        var i, taskmanagertabcontent, taskmanagertablinks;
        taskmanagertabcontent = document.getElementsByClassName("taskmanagertabcontent");
        for (i = 0; i < taskmanagertabcontent.length; i++) {
            taskmanagertabcontent[i].style.display = "none";
        }
        taskmanagertablinks = document.getElementsByClassName("taskmanagertablinks");
        for (i = 0; i < taskmanagertablinks.length; i++) {
            taskmanagertablinks[i].className = taskmanagertablinks[i].className.replace(" active", "");
        }
        document.getElementById(navtaskmanagertabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

    // Get the element with id="defaultOpen" and click on it
    document.getElementById("defaultOpen").click();

// <!-- script to show/hide paylater & All messages section -->
