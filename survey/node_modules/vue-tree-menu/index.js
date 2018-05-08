import treeMenuComponent from './treeMenu.vue'

const VueTreeMenu = {
    install: function(Vue) {
        Vue.component('treeMenu', treeMenuComponent)
    }
}

export default VueTreeMenu