<template>
    
  <v-data-table :headers="headers" :items="ubigeo" sort-by="ID_ubigeo" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
      <v-toolbar-title class="subheading blue--text">UBIGEO</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="500px">

          <template v-slot:activator="{ on, attrs }">
            
            <v-btn color="blue" dark class="mb-2" v-bind="attrs" v-on="on">
              Agregar código de Ubigeo
            </v-btn>

          </template>

          <v-card>
            <v-card-title>
              <span class="text-h5 blue--text">{{ formUbigeo }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_ubigeo"
                      label="Código Ubigeo"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nombre_departamento"
                      label="Departamento"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nombre_provincia"
                      label="Provincia"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nombre_distrito"
                      label="Distrito"
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
  var url = 'http://127.0.0.1:5000/ubigeo';
  export default {
    data: () => ({
      config_request: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },          
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'Código Ubigeo', value: 'ID_ubigeo' },
        { text: 'Departamento', value: 'Nombre_departamento' },
        { text: 'Provincia', value: 'Nombre_provincia' },
        { text: 'Distrito', value: 'Nombre_distrito' },
        { text: 'Acciones', value: 'actions', sortable: false },
      ],
      ubigeo: [],
      editedIndex: -1,
      editedItem: {
        ID_ubigeo : '',
        Nombre_departamento : '',
        Nombre_provincia : '',
        Nombre_distrito : '',
      },
      defaultItem: {
        ID_ubigeo : '',
        Nombre_departamento : '',
        Nombre_provincia : '',
        Nombre_distrito : '',
      },
    }),

    computed: {
      formUbigeo () {
        return this.editedIndex === -1 ? 'Nuevo código Ubigeo' : 'Editar código Ubigeo'
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
        this.ubigeo = [
            {
            ID_ubigeo : "010401",
            Nombre_departamento : "76918799",
            Nombre_provincia : "Fabricio",
            Nombre_distrito : "Centeno",
          },
        ]
      },

      getItems () {
        axios.get(url, {
          headers: this.config_request
        })
        .then(response => {
          this.ubigeo = response.data
        })
        .catch(error => {
          console.log(error)
        })
      },

      actionEdit (item) {
        this.editedIndex = this.ubigeo.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.ubigeo.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(url + '/' + this.editedItem.ID_ubigeo, {
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
          this.ubigeo.push(response.data)
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
        // this.ubigeo.push(this.editedItem)
      },

      editItem (){
        axios.put(url+'/editar/'+this.editedItem.ID_ubigeo, this.editedItem, {
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
          // Object.assign(this.ubigeo[this.editedIndex], this.editedItem)
        } else {
          console.log("crear")
          this.addItem()
          // this.ubigeo.push(this.editedItem)
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


