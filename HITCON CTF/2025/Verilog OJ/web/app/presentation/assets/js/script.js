const { MDCTopAppBar } = mdc.topAppBar;
const { MDCDrawer } = mdc.drawer;
const { MDCRipple } = mdc.ripple;

const $topAppBar = document.querySelector('.mdc-top-app-bar');
const topAppBar = new MDCTopAppBar($topAppBar);
$topAppBar.addEventListener('MDCTopAppBar:nav', ev => {
drawer.open = !drawer.open;
})

const $drawer = document.querySelector('.mdc-drawer');
const drawer = new MDCDrawer($drawer);

const $$ripple = document.querySelectorAll('.mdc-button, .mdc-icon-button, .mdc-deprecated-list-item');
$$ripple.forEach(el => {
const ripple = new MDCRipple(el);
});
