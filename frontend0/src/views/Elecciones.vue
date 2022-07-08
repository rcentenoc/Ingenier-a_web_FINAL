<template>
    
  <v-data-table :headers="headers" :items="elecciones" sort-by="Apellidos_elector" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
      <v-toolbar-title class="subheading blue--text">ELECCIONES</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="400px">

          <template v-slot:activator="{ on, attrs }">
            
            <v-btn color="blue" dark class="mb-2" v-bind="attrs" v-on="on">
              Agregar elector
            </v-btn>

          </template>

          <v-card>
            <v-card-title>
              <span class="text-h5 blue--text">{{ fomrEleccion }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.ID_eleccion"
                      label="ID de la elección"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Nombre_eleccion"
                      prepend-icon="person" label="Nombre de la elección"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="12">

                    <v-text-field v-model="editedItem.Fecha_eleccion"
                      label="Fecha a realizar la elección"
                      hint="YYYY/MM/DD format"
                      persistent 
                      prepend-icon="event" 
                      @blur="date = parseDate(dateFormatted)" 
                      v-on="on">
                    ></v-text-field>

                  </v-col>

                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn color="red darken-1" text @click="close">
                Cancelar
              </v-btn>

              <v-btn color="green darken-1" text @click="save">
                Guardar
              </v-btn>

            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">¿Estas seguro de eliminar este item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="closeDelete">Cancelar</v-btn>
              <v-btn color="green darken-1" text @click="deleteItemConfirm">Confirmar</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>

    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        small
        class="mr-2" color="green"
        @click="actionEdit(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small color="red"
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Actualizar
      </v-btn>
    </template>

  </v-data-table>
</template>

<script>
  import axios from 'axios';
  var url = 'http://127.0.0.1:5000/eleccion';
  export default {
    data: () => ({
      config_request: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },          
      dialog: false,
      dialogDelete: false,
      menu1: false,
      
      headers: [
        { text: 'ID', value: 'ID_eleccion' },
        { text: 'Elección', value: 'Nombre_eleccion' },
        { text: 'Fecha de elección', value: 'Fecha_eleccion' },
        { text: 'Acciones', value: 'actions', sortable: false },
      ],
      elecciones: [],
      editedIndex: -1,
      editedItem: {
        ID_eleccion: 0,
        Nombre_eleccion: '',
        Fecha_eleccion: '',
      },
      defaultItem: {
        ID_eleccion: 0,
        Nombre_eleccion: '',
        Fecha_eleccion: '',
      },
    }),

    computed: {
      fomrEleccion () {
        return this.editedIndex === -1 ? 'Nueva Elección' : 'Editar Elección'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    created () {
      // this.initialize()
      this.getItems()
    },

    methods: {
      initialize () {
        this.elecciones = [
          {
            ID_elector : "sha40ty356",
            DNI_elector : "26568789",
            Nombre_elector : "Silvip",
          },
        ]
      },

      getItems () {
        axios.get(url, {
          headers: this.config_request
        })
        .then(response => {
          this.elecciones = response.data
        })
        .catch(error => {
          console.log(error)
        })
      },

      actionEdit (item) {
        this.editedIndex = this.elecciones.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.elecciones.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(url + '/' + this.editedItem.ID_eleccion, {
          headers: this.config_request
        })
        .then(response => {
          this.getItems()
          this.closeDelete()
        })
        .catch(error => {
          console.log(error)
        })
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
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

      editItem (){
        axios.put(url+'/editar/'+this.editedItem.ID_eleccion, this.editedItem, {
          headers: this.config_request
        })
        .then(response => {
          this.getItems()
          this.close()
        })
        .catch(error => {
          console.log(error)
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

      parseDate(date){
        if(!date) return null
        const [day, month, year] = date.split('/');
        return `${day.padStart(2,'0')}-${month.padStart(2,'0')}-${year}`;
      },
    },
  }
</script>


