<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="400px">
            <template v-slot:activator="{on}">
                <v-btn outlined color="blue lighten-2" dark v-on="on">
                    Agregar Elección
                </v-btn>
            </template>
            <v-card>

                <v-card-title>
                    <span class="headline">Nueva Elección</span>
                </v-card-title>

                <v-form class="px-3" ref="form">
                    <v-card-text>

                        <v-col cols="12" sm="6" md="12">
                            <v-text-field v-model="editedItem.ID_eleccion" label="ID de la elección"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="12">
                            <v-text-field v-model="editedItem.Nombre_eleccion" label="Nombre de la elección"></v-text-field>
                        </v-col>
                          
                        <v-col cols="12" lg="6">
                            <v-menu ref="menu1" v-model="editedItem.Fecha_eleccion" :close-on-content-click="false" transition="scale-transition" offset-y max-width="290px" min-width="290px">
                                
                                <template v-slot:activator="{on}">
                                    <v-text-field 
                                    v-model="dateFormatted" 
                                    label="Fecha a realizar la elección" 
                                    hint="MM/DD/YYYY format"
                                    persistent 
                                    prepend-icon="event" 
                                    @blur="date = parseDate(dateFormatted)" 
                                    v-on="on">
                                    </v-text-field>
                                </template>

                                <v-date-picker v-model="date" no-title @input="menu1 = false" >

                                </v-date-picker>
                            </v-menu>
                        </v-col>

                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color=" blue darken-1" text @click="dialog = false">Cerrar</v-btn>
                        <v-btn color="green" text outlined @click="save">Guardar</v-btn>
                    </v-card-actions>
                </v-form>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
    import axios from 'axios';
    var url = 'http://127.0.0.1:5000/eleccion';
    export default{
        data: vm =>({
            dialog: false,
            dialogDelete: false,
            title: '',
            config_request: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            elecciones: [],
            editedIndex: -1,  
            editedItem: {
                ID_eleccion: '',
                Nombre_eleccion: '',
                Fecha_eleccion: '',
            },
            defaultItem: {
                ID_eleccion: '',
                Nombre_eleccion: '',
                Fecha_eleccion: '',
            },
            content: '',
            due:null,
            date: new Date().toISOString().substr(0, 10),
            dateFormatted: vm.formatDate(new Date().toISOString().substr(0, 10)),
            menu1: false,
            inputRules: [
                v => v.length >= 3 || 'Title must be at least 3 characters',
            ]
        }),
        methods: {
            formatDate(date){
                if(!date) return null
                const [year, month, day] = date.split('-');
                return `${year}/${month}/${day}`;
            },
            parseDate(date){
                if(!date) return null
                const [year, month, day] = date.split('/');
                return `${year}-${month.padStart(2,'0')}-${day.padStart(2,'0')}`;
            },
            addItem () {
                axios.post(url+'/nuevo', this.editedItem, {
                headers: this.config_request
                })
                .then(response => {
                this.elecciones.push(response.data)
                this.close()
                })
                .catch(error => {
                console.log(error)
                })
                // this.elecciones.push(this.editedItem)
            },
            close () {
                this.dialog = false
                this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
                })
            },
            save () {
                if (this.editedIndex > -1) {
                console.log("editar")
                this.editItem()
                // Object.assign(this.elecciones[this.editedIndex], this.editedItem)
                } else {
                console.log("crear")
                this.addItem()
                // this.elecciones.push(this.editedItem)
                }
                this.close()
            },

        },
        computed:{
            computedDateFormatted(){
                return this.formatDate(this.date);
            }
        },
        watch: {
            date(){
                this.dateFormatted = this.formatDate(this.date);
            }
        },
    }
</script>