$(document).ready(function () {
//    var socket = io.connect('http://192.168.0.90:5009');
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    // socket.emit('input_image', ' ');

    socket.on('from_flask', function (data) {
        console.log('1111');
        // console.log(data)
        if (data != null) {
            var list_image = data.split('$');
            $("#imageElement").attr("src", list_image[0]);
            for (var i = 1; i < list_image.length; i++) {
                var row = list_image[i].split('|');
                console.log(row);
                var img_id = '#img_' + row[1];
                var _img_id = 'img_' + row[1];
                var time_id = "time_" + row[1];
                var temp_id = "temp_" + row[1];
                var today = new Date();
                var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
                var time = today.getHours() + ":" + today.getMinutes()
                // + ":" + today.getSeconds();
                var dateTime = date + ' ' + time;
                var temp_str = (parseFloat(row[2]) + parseFloat(row[3])).toFixed(2).toString()                // dateTime = new Date().toLocaleString("en-US", {timeZone: "Asia/Tokyo"})
                $(img_id).attr("src", "data:image/jpeg;base64," + row[0]);
                document.getElementById(_img_id).style.visibility = 'visible';
                document.getElementById(time_id).innerHTML = dateTime;
                document.getElementById(time_id).style.visibility = 'visible';
                document.getElementById(temp_id).innerHTML = temp_str;
                document.getElementById(temp_id).style.visibility = 'visible';
            }
        }
    });


//    function sendSnapshot() {
//        console.log('2222');
//        socket.emit('input_image', ' ');
//    }
//
//    $(document).ready(function myFunction() {
//        setInterval(function () {
//            sendSnapshot();
//        }, 50);
//    })


    $('#btn-clear-all').click(function () {
        for (var i = 0; i < 12; i++) {
            var img_id = "img_" + (i + 1);
            var time_id = "time_" + (i + 1);
            var temp_id = "temp_" + (i + 1);
            console.log(img_id);
            document.getElementById(img_id).style.visibility = 'hidden';
            document.getElementById(time_id).style.visibility = 'hidden';
            document.getElementById(temp_id).style.visibility = 'hidden';
        }
        $.ajax({
            url: '/clean',
            data: {},
            type: 'POST',
            success: function (data) {
                console.log('Register successfully!:' + data);
            },
            error: function (error) {
                console.log('Register Erro:' + error);
            }
        });

    });

    $('#btn-adjust-temp').click(function () {
        var temp_delta = document.getElementById("text-adjust-temp").value
        console.log('text!:' + temp_delta);
        $.ajax({
            url: '/auto/temperature',
            data: {person_temp: temp_delta},
            type: 'POST',
            success: function (data) {
                console.log(data)
            },
            error: function (error) {
                console.log('Temperature Erro:' + error);
            }
        });

    });

    $('#btn-adjust-register').click(function () {
        var temp_detect = document.getElementById("text-adjust-register").value
        console.log('text!:' + temp_detect);
        $.ajax({
            url: '/register/temperature',
            data: {temp_detect: temp_detect},
            type: 'POST',
            success: function (data) {
                for (var i = 0; i < data['list_id'].length; i++) {
                    var temp_id = 'temp_' + data['list_id'][0];
                    var img_id = "img_" + data['list_id'][0];
                    var time_id = "time_" + data['list_id'][0];
                    document.getElementById(img_id).style.visibility = 'hidden';
                    document.getElementById(time_id).style.visibility = 'hidden';
                    document.getElementById(temp_id).style.visibility = 'hidden';
                }
                console.log('Temperature register successfully!:' + data);
            },
            error: function (error) {
                console.log('Temperature register Error:' + error);
            }
        });

    });

});

