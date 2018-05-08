import rippleComponent from './ripple.vue'

const VueRipple = {
    install: function (Vue) {
        Vue.component('ripple', rippleComponent)
    } 
}  

export default VueRipple
