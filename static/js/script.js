
function pushData(arr) {
    // returns a list of dt/dd pairs from a two-dimensional array
    let stats = [];
    for (i = 0; i < arr.length; i++) {
        stats.push("<dt>" + arr[i][0] + "</dt><dd>" + arr[i][1] + "</dd>");
    }
    return stats;
}

//mobile menu toggle
const mobilemenu = document.getElementById('m-btn');
mobilemenu.addEventListener('click', function() {
    console.log('togglemenu');
    document.getElementById('menu-list').classList.toggle("show");
});


const comments = document.querySelectorAll('.comment');
if ( comments.length > 0 ){
    //update comment count
    document.getElementById('comment-count').innerText = comments.length;
}

console.log("hello");
const dither_icons = document.querySelectorAll('.dither-toggle');
dither_icons.forEach(icon => {
	icon.addEventListener('click', function() {
	    let figure = icon.closest('.figure-controls').previousElementSibling;
	    let img = figure.querySelector('img');

	    if( figure.getAttribute('data-imgstate') == "dither"){
	    	figure.setAttribute('data-imgstate', 'undither');	    	
	    	let original = img.getAttribute('data-original');
	    	img.src = original;
	    }else{
	    	figure.setAttribute('data-imgstate', 'dither');
	    	let dither= img.getAttribute('data-dither');
	    	img.src = dither;
	    }    
	});
});
