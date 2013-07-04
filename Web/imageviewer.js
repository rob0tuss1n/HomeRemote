var files, current, imgdir;
function imageviewer(dir) {
    imgdir = dir;
    current = 2;
    $.get("data/security.php?action=getsnapnames&folder="+imgdir, function(data) {
        files = JSON.parse(data);
        $("#image-view").attr("src", "cams/"+imgdir+"/"+files[current]);
        $("#name").html(files[current]);
        $("#gallery").dialog({
            height: 560,
            width: 700
        });
        $("#gallery").disableSelection();
    });
}
function nextSnapshot() {
    if(files[current + 1] != null) {
        current = current + 1;
        $("#image-view").attr("src", "cams/"+imgdir+"/"+files[current]);
        $("#name").html(files[current]);
    }
}
function lastSnapshot() {
    if(files[current -1] != null && files[current-1] != "." && files[current-1] != "..") {
        current = current - 1;
        $("#image-view").attr("src", "cams/"+imgdir+"/"+files[current]);
        $("#name").html(files[current]);
    }
}