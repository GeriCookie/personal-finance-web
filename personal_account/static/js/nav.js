$(function() {
    var $dropdowns = $('.has-dropdown');
    $dropdowns.find('.dropdown-toggle').on('click', function(ev) {
        var $this = $(this);
        var $dropdownList = $this.next(".list-dropdown");
        console.log($dropdownList);
        $dropdownList.toggleClass('hidden');
    });
});

/*
<li class="list-item has-dropdown">
    <a class="dropdown-toggle" href="#">User</a>
    <ul class="list list-dropdown">
        <li>
            <a href="/accounts/signup">Sign up</a>
        </li>
        <li>
            <a href="/accounts/login">Sign in</a>
        </li>
    </ul>
</li>
*/