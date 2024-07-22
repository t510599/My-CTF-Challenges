/**
 * document query selector
 * @param {*} selector - select
 * @param {*} ctx - context
 * @returns {HTMLElement} ctx.querySelector(selector)
 */
const dqs = (selector, ctx = document) => {
    return ctx.querySelector(selector);
}

/**
 * document query selector
 * @param {*} selector - select
 * @param {*} ctx - context
 * @returns {NodeListOf<HTMLElement>} ctx.querySelectorAll(selector)
 */
const dqsa = (selector, ctx = document) => {
    return ctx.querySelectorAll(selector);
}

/**
 * document query selector of HTMLElement
 * @param {*} selector 
 * @returns {HTMLElement} this.querySelector(selector)
 */
HTMLElement.prototype.dqs = function(selector) {
    return dqs(selector, this);
}

/**
 * document query selector of HTMLElement
 * @param {*} selector 
 * @returns {NodeListOf<HTMLElement>} this.querySelectorAll(selector)
 */
HTMLElement.prototype.dqsa = function(selector) {
    return dqsa(selector, this);
}

/**
 * alias for addEventListener
 * @param {*} event - event name
 * @param {*} callback - event callback
 * @param {*} options - event options
 * @returns {HTMLElement} this
 */
HTMLElement.prototype.on = function(event, callback, options={}) {
    this.addEventListener(event, callback, options);
    return this;
}

/**
 * alias for removeEventListener
 * @param {*} event - event name
 * @param {*} callback - event callback
 * @param {*} options - event options
 * @returns {HTMLElement} this
 */
HTMLElement.prototype.off = function(event, callback, options={}) {
    this.removeEventListener(event, callback, options);
    return this;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}