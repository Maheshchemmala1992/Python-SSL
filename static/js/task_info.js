// $( document ).ready(function() {
//     $('.val_id').click(function(){
//         var task_id = $('.task_id').val;
//         console.log('-----task id after buton click-------', document.querySelectorAll('.task_id').value)
//         $.ajax({
//             method:'GET',
//             url:'/task/'+ task.id +'/view',
//             success: function(data) {
//                 console.log('data---------',data);
//             },
//             failure: function(data) { 
//                 console.log('Got an error dude');
//             }
//         });
//     })
// });

var catid = document.querySelectorAll(`.detail_task`);
catid.forEach(pd => {
    pd.addEventListener("click", () => {
        let cat_id = pd.value
        const xhr = new XMLHttpRequest();
        xhr.responseType = "json";
        xhr.open('GET', `/task/${cat_id}/view`);
        xhr.onload = () => {
            const cat_info = xhr.response['task_info'];
            // console.log('-------------', cat_info)
            document.getElementById('task_status').value = cat_info.task_status
            document.getElementById('planned_start_date').value = cat_info.planned_start_date
            document.getElementById('planned_end_date').value = cat_info.planned_end_date
            document.getElementById('actual_start_date').value = cat_info.actual_start_date
            document.getElementById('actual_end_date').value = cat_info.actual_end_date
            document.getElementById('priority').value = cat_info.actual_end_date
            document.getElementById('description').value = cat_info.description
            document.getElementById('created_date').innerHTML = cat_info.created_on
            document.getElementById('title').innerHTML = cat_info.title
        };
        xhr.send();
    })
})
