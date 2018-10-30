Vue.component('text-editor', {
    props: ['value'],
    watch: {
        value: function (val) {
            if (val != this.textEditor.getValue()) {
                this.textEditor.setValue(val ? val : '');
            }
        },
    },
    mounted: function () {
        var scope = this;
        this.textEditor = CodeMirror.fromTextArea(document.getElementById('text_editor'), {
            lineNumbers: true
        });
        this.textEditor.on('change', function (cm) {
            scope.textEditor.save();
            scope.$emit('input', cm.getValue())
        });
        this.textEditor.setValue(this.value ? this.value : '');
        this.textEditor.setSize("100%", "100%");
    },
    template: '<textarea id="text_editor"></textarea>'
})

ListWithSearchComponent = {
    template: `
            <div>
                <div class="input-group">
                    <input v-model="query" v-on:keyup.enter="search" type="text" class="form-control form-control-sm" placeholder="Search...">
                    <div class="input-group-append">
                        <button v-on:click="search" class="btn btn-sm btn-outline-secondar" type="button">Search <div v-if="isSearching" class="loader"></div></button>
                    </div>
                </div>
                <ul class="ul-items">
                    <li v-for="(item, index) in results" @click="selectItem(item, index)">
                        <a v-bind:class="{'active': item == selectedItem}" class="nav-link" href="#">{{item.name}}</a>
                    </li>
                </ul>
            </div>
          `,
    props: ['url'],
    data: function () {
        return {
            query: '',
            results: [],
            noResults: false,
            isSearching: false,
            error: '',
            selectedItem: null,
        }
    },
    mounted: function () {
        this.search();
    },
    methods: {
        selectItem: function (item, index) {
            this.selectedItem = item;
            this.selectedItemIndex = index;
            this.$emit('select-item', { 'item': this.selectedItem, 'index': this.selectedItemIndex })
        },
        search: function () {
            this.isSearching = true;
            this.error = '';
            fetch(`${this.url}?q=${encodeURIComponent(this.query)}`)
                .then(res => res.json())
                .then(res => {
                    this.isSearching = false;
                    this.results = res;
                    this.noResults = this.results.length === 0;
                })
                .catch(error => {
                    this.isSearching = false;
                    this.results = [];
                    this.noResults = false;
                    this.error = "Error while connection to the server. " + error.message;
                });
        },
        delete: function (index, item) {
            if (index > -1 && item) {
                this.$delete(this.results, index)
            }
        },
        refresh: function (index, item) {
            if (index > -1 && item) {
                this.$set(this.results, index, item);
            }
        },
    }
}