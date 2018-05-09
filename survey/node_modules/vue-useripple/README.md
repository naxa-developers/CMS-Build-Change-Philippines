# vue-useripple

> A ripple plugin of Vue.js

[Demo](https://ldq-first.github.io/vue-ripple-plugin/dist/#/)

[more detail of use](https://github.com/LDQ-first/vue-ripple-plugin/tree/master/src/views/show.vue)

## Use
``` javascript
/*-- npm --*/
npm install --save vue-useripple

```

``` javascript
/*-- main.js --*/
import Vue from 'vue'
import VueRipple from 'vue-useripple'
Vue.use(VueRipple)
```

``` 
/*-- vue --*/
/*-- Fisrt --*/
<template>
    <div>
        <ripple :isInline="isInline">
            <button slot="pure" @click="clickEvent">button</button>
        </ripple>
    </div>
</template>
```

```
/*-- vue --*/
/*-- Second --*/
<template>
    <div>
        <ripple children="one">
            <div slot="children" >
                <button @click="clickEvent">button</button>
            </div>
        </ripple>
    </div>
</template>
```

```
/*-- vue --*/
/*-- Third --*/
<template>
    <div>
       <ripple children="one">
            <div slot="children" class="children">
                <footer>
                    <ripple  :isInline="isInline">
                        <button slot="pure"  @click="clickEvent">showModal</button>
                    </ripple>
                </footer>
            </div>
        </ripple>
    </div>
</template>
```

```
/*-- vue --*/
/*-- Fourth --*/
<template>
    <div>
        <ripple :isInline="isInline" speed="2">
            <button slot="pure">speed</button>
        </ripple>
        <ripple :isInline="isInline" bg="#2B72D6">
            <button slot="pure">background</button>
        </ripple>
        <ripple :isInline="isInline" :br="br">
            <button slot="pure">borderRadius</button>
        </ripple>
    </div>
</template>
```

## param


``` javascript
/*
    make ripple become inline-block
*/
isInline: {       
    type: Boolean,
    required: false
},
/*
    set speed of ripple 
*/
speed: {
    type: String,
    required: false
},
/*
    set background of ripple 
*/
bg: {
    type: String,
    required: false
},
/*
    change ripple to circle
*/
br: {
    type: Boolean,
    required: false   
},
/*
    raise z-index of child element  
*/
children: {
    type: String,
    required: false
}
```
