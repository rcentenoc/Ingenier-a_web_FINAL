<template>
    
  <v-data-table :headers="headers" :items="partidos" sort-by="ID_siglas_partido_politico" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
      <v-toolbar-title class="subheading blue--text">AGRUPACIONES POLÍTICAS</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="500px">

          <template v-slot:activator="{ on, attrs }">
            
            <v-btn color="blue" dark class="mb-2" v-bind="attrs" v-on="on">
              Agregar partido político
            </v-btn>

          </template>

          <v-card>
            <v-card-title>
              <span class="text-h5 blue--text">{{ formPartidos }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_siglas_partido_politico"
                      label="ID"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Nombre_partido_politico"
                      label="Nombre del Partido político"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Foto_partido_politico"
                      label="Logo"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Direción_partido_politico"
                      label="Dirección"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Web_partido_politico"
                      label="Pagina web del partido político"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nombre_departamento"
                      label="Departamento de origen"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_ubigeo"
                      label="Código Ubigeo"
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
  var url = 'http://127.0.0.1:5000/partido_politico';
  export default {
    data: () => ({
      config_request: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },          
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'ID', value: 'ID_siglas_partido_politico' },
        { text: 'Nombre', value: 'Nombre_partido_politico' },
        { text: 'Logo', value: 'Foto_partido_politico' },
        { text: 'Dirección', value: 'Direción_partido_politico' },
        { text: 'Web', value: 'Web_partido_politico' },
        { text: 'Nombre', value: 'Nombre_departamento' },
        { text: 'Ubigeo', value: 'ID_ubigeo' },
        { text: 'Acciones', value: 'actions', sortable: false },
      ],
      partidos: [],
      editedIndex: -1,
      editedItem: {
        ID_siglas_partido_politico: '',
        Nombre_partido_politico: '',
        Foto_partido_politico: '',
        Direción_partido_politico: '',
        Web_partido_politico: '',
        Nombre_departamento: '',
        ID_ubigeo: '',
      },
      defaultItem: {
        ID_siglas_partido_politico: '',
        Nombre_partido_politico: '',
        Foto_partido_politico: '',
        Direción_partido_politico: '',
        Web_partido_politico: '',
        Nombre_departamento: '',
        ID_ubigeo: '',
      },
    }),

    computed: {
      formPartidos () {
        return this.editedIndex === -1 ? 'Nuevo partido político' : 'Editar partido político'
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
        this.partidos = [
            {
            ID_siglas_partido_politico : "",
            Nombre_partido_politico : "",
            Foto_partido_politico : "",
            Direción_partido_politico : "",
            Web_partido_politico : "",
            Nombre_departamento : "",
            ID_ubigeo : "",
          },
        ]
      },

      getItems () {
        axios.get(url, {
          headers: this.config_request
        })
        .then(response => {
          this.partidos = response.data
        })
        .catch(error => {
          console.log(error)
        })
      },

      actionEdit (item) {
        this.editedIndex = this.partidos.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.partidos.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(url + '/' + this.editedItem.ID_siglas_partido_politico, {
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
          this.partidos.push(response.data)
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
        // this.partidos.push(this.editedItem)
      },

      editItem (){
        axios.put(url+'/editar/'+this.editedItem.ID_siglas_partido_politico, this.editedItem, {
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
          // Object.assign(this.partidos[this.editedIndex], this.editedItem)
        } else {
          console.log("crear")
          this.addItem()
          // this.partidos.push(this.editedItem)
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


