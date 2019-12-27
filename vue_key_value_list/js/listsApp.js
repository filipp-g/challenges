var listsApp = new Vue({
    el: '#lists-app',
    data: {
        error: '',
        input: '',
        nameValues: [
            {name: 'goldfish', value: 'bowl'},
            {name: 'sharks', value: 'tornados'}
        ],
        selected: {}
    },
    methods: {
        validateInput: function (input) {
            this.error = '';
            if (((input.match(/=/g) || []).length) !== 1) {
                this.error = 'Input must contain 1 and only 1 equals ("=")';
            } else if (input.match(/[^A-Za-z0-9 =]/)) {
                this.error = 'Input must contain only alphanumeric chars (and "=")';
            } else {
                let validated = input.replace(new RegExp(' ', 'g'), '').split('=');
                if (validated[0] === '' || validated[1] === '') {
                    this.error = 'Both sides of equals ("=") cannot be blank';
                } else if (this.nameValues.find(x => x.name === validated[0])) {
                    this.error = 'Name "' + validated[0] + '" is already present in list';
                }
            }
            return this.error ? false : {name: validated[0], value: validated[1]};
        },
        addItem: function () {
            let validPair = this.validateInput(this.input);
            if (validPair) {
                this.nameValues.push(validPair);
                this.input = '';
            }
        },
        remove: function () {
            const index = this.nameValues.indexOf(this.selected);
            if (index > -1) {
                this.nameValues.splice(index, 1);
            }
        },
        clear: function () {
            this.nameValues = [];
        },
        exportJSON: function () {
            let content = JSON.stringify(this.nameValues);
            let a = document.createElement('a');
            let file = new Blob([content], {type: 'text/plain'});
            a.href = URL.createObjectURL(file);
            a.download = 'name-value-list.json';
            a.click();
        },
        sortByName: function () {
            this.nameValues.sort((a, b) => a.name > b.name);
        },
        sortByValue: function () {
            this.nameValues.sort((a, b) => a.value > b.value);
        },
        setSelected: function (item) {
            this.selected = item;
        }
    }
});
