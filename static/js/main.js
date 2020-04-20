$(document).ready(function () {
    // Make all the buttons black by changing the class

    $('.progress').css("display", "none");
    $('.loader').css("display", "none");
    $('.datepicker').datepicker();
    $(document).ready(function () {
        $('.tooltipped').tooltip({
            html: true
        });
    });
    $(document).ready(function () {
        $('select').formSelect();
    })

    $('.chips').chips();

    
    $('#string_chips').click(function(){
        $("#tags").val(JSON.stringify(M.Chips.getInstance($('#chips_tags')).chipsData)));
   });

    path = location.pathname.replace("/", "")
    // check if the location is like contract/contractId
    if (path.indexOf("trading1") == -1) {
        $('.' + path + 'Path').addClass('active activePath')
    }

    // Get the current Participant
    curParUrl = "http://localhost:3000/api/system/ping"
    $.ajaxCallaf(curParUrl, "GET", "", function (output) {
        if (output.status) {
            currentIdentityFull = output.output.participant
            // check if the user is admin
            if (currentIdentityFull.indexOf("admin") >= 0) {
                admin = true
                $('#currentParticipant').text("Administrator")
                $('#currentDesignation').remove()
                $('#accountBalanceNav').remove()
                $('.currentLoggedInLoader').css("display", "none")
                $('#nav-mobile').append('<li class="subheader1 exportPath"><a class="subheader1a" href="/export"> <i class="material-icons black-text text-darken-4">cloud_download</i>Export Card</a></li>')
            }
            // else
            else {
                admin = false
                currentIdentity = currentIdentityFull.replace('org.example.energy.Building#', '');
                // Get the Account balance

            }

        } else {
            if (output.output.status == "500") {
                M.toast({
                    html: 'Please Login first.'
                })
            }

        }
    })


    // Upload your resume
    $(document).on("click", "#uploadresume", function () {

        var baseUrl = "http://localhost:3000/api/resume/import";
        var data = new FormData();
        data.append('card', $('#formfile')[0].files[0])

        // Call the rest api endpoint for uploading a resume
        $.ajax({
            url: baseUrl,
            type: "POST",
            data: data,
            processData: false,
            contentType: false,
            xhrFields: {
                withCredentials: true
            },
            success: function (resp) {
                M.toast({
                    html: 'Uploaded Successfully!'
                })
                $(location).attr('href', "/");
            },
            error: function (resp) {
                M.toast({
                    html: 'Upload failed!'
                })
            },
        });
    })


})