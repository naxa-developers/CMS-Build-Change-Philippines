<template>
    <li  v-if="!isEmptyObj(list)">
        <div>
            <ripple>
                <button slot="pure" class="item-btn" :class="{parent: isFolder}"
                 @click="toggle" >
                    <span class="name">
                        <span class="item-icon" v-if="menuIcon">
                            <img class="icon" src="./icon/open.svg" v-if="spread"></img>
                            <img class="icon" src="./icon/close.svg" v-else></img>
                        </span>
                        {{list.name}}
                    </span>
                    <div class="constrol">
                        <span @click.stop="changeType" class="addChild" v-if="addbtn">{{AddText}}</span>
                        <span @click.stop="deleteChild" class="deleteChild" v-if="deletebtn && !this.list.root">{{DeleteText}}</span>
                        <span v-if="isFolder">
                            <img class="icon" src="./icon/unfold.svg" v-if="spread"></img>
                            <img class="icon" src="./icon/fold.svg" v-else></img>
                        </span>
                    </div>
                </button>
            </ripple>
        </div>
        <ul v-show="spread" v-if="isFolder" class="list">
            <treeMenu v-for="(list, index) in list.children" 
            key="index"  class="item"  :list="list" :menuIcon="menuIcon" :name="name" :addText="addText" :deleteText="deleteText"
            addbtn="addbtn" deletebtn="deletebtn" add="add">
            </treeMenu>
            <ripple :isInline="true" class="addripple" bg="#F35286" speed="1" v-if="add">
                <li slot="pure" class="add" @click="addChild"> + </li>
            </ripple>
        </ul>
    </li>
</template>

<script>
    import Vue from 'vue'
    export default {
        props: {
            list: {
                type: Object,
                required: true
            },
            menuIcon: {
                type: Boolean,
                required: true
            },
            name: {
                type: String,
                required: false
            },
            addText:{
                type: String,
                required: false
            },
            deleteText: {
                type: String,
                required: false
            },
            add: {
                type: Boolean,
                required: false
            },
            deletebtn: {
                type: Boolean,
                required: false
            },
            addbtn: {
                type: Boolean,
                required: false
            }

        },
        data () {
            return {
                spread: false,
                AddText: this.addText || 'add',
                DeleteText: this.deleteText || 'delete'
            }
        },
        computed: {
            isFolder () {
                return this.list.children && this.list.children.length
            }
        },
        methods: {
            toggle () {
                if (this.isFolder) {
                    this.spread = !this.spread
                }
            },
            changeType () {
                if(!this.isFolder) {
                    Vue.set(this.list, 'children', [])
                    this.addChild()
                    this.spread = true
                }
            },
            addChild () {
                this.list.children.push({
                    name: this.name || 'new item'
                })
            },
            deleteChild () {
                for(let key in this.list) {
                    Vue.delete(this.list, key)
                }
            },
            isEmptyObj (obj) {
                for(let e in obj) {
                    return false
                }
                return true
            }
        }
    }
    
</script>

<style lang="scss" scoped>
    .list {
        min-height: 40px;
        flex-flow: column wrap;
        overflow: hidden;
        background: #FFF;
        transition: all .4s cubic-bezier(.25,.8,.25,1);
        .item {
             padding-left: 1em;
        }
    }
    .parent {
        font-weight: bold;
    }
    .addripple {
        margin: 16px;
        box-shadow: 0 1px 6px rgba(0,0,0,.4),
                    0 1px 4px rgba(0,0,0,.2);
        .add {
            background: #CCC;
            width: 20px;
            line-height: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 5px;
            cursor: pointer;
            
        }
    }   
    .item-icon {
        margin-right: 10px;
    }
    .icon {
        width: 20px;
        height: 20px;
        display: inline-block;
        vertical-align: middle;
    }
    .item-btn {
        cursor: pointer;
        border: none;
        outline: none;
        -webkit-appearance: none;
        color: #000;
        overflow: hidden;
        background: #FFF;
        height: 40px;
        line-height: 40px;
        padding: 0 16px;
        border-radius: 0;
        min-width: 88px;
        width: 100%;
        box-shadow: 0 1px 6px rgba(0,0,0,.4),
                    0 1px 4px rgba(0,0,0,.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        &:hover {
            background: rgba(77, 175, 229, 0.4);
            .constrol {
                .addChild {
                    display: inline-block;
                }
                .deleteChild {
                    display: inline-block;
                }
            }
        }
        .constrol  {

            .addChild {
                display: none;
            }
            .deleteChild {
                display: none;
                &:hover {
                    color: red;
                }
            }
            
        }
        
       
    }
</style>