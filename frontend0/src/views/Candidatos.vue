<template>
    
  <v-data-table :headers="headers" :items="candidatos" sort-by="ID_candidato" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
      <v-toolbar-title class="subheading blue--text">CANDIDATOS ELECTORALES</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="500px">

          <template v-slot:activator="{ on, attrs }">
            
            <v-btn color="blue" dark class="mb-2" v-bind="attrs" v-on="on">
              Agregar Candidato 
            </v-btn>

          </template>

          <v-card>
            <v-card-title>
              <span class="text-h5 blue--text">{{ formCandidato }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.ID_candidato" 
                      label="ID del Candidato"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="8">
                    <v-text-field v-model="editedItem.ID_partido_politico"
                      label="ID de la Agrupación política"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_candidato_elector"
                      label="ID de elector"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.DNI_candidato_elector"
                      label="DNI"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Nombre_candidato_elector"
                      label="Nombre del candidato"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Apellidos_candidato_elector"
                      label="Apellidos del candidato"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Foto_candidato"
                      label="Foto"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Hoja_de_vida_candidato"
                      label="Enlace de Hoja de vida"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Propuesta_candidato"
                      label="Enlace de Propuestas"
                    ></v-text-field>
                  </v-col>
                  

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nombre_departamento"
                      label="Departamento de origen"
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
  var url = 'http://127.0.0.1:5000/candidato';
  export default {
    data: () => ({
      config_request: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },          
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'ID', value: 'ID_candidato' },
        { text: 'ID elector', value: 'ID_candidato_elector' },
        { text: 'DNI', value: 'DNI_candidato_elector' },
        { text: 'Agrupación Política', value: 'ID_partido_politico' },
        { text: 'Nombre', value: 'Nombre_candidato_elector' },
        { text: 'Apellidos', value: 'Apellidos_candidato_elector' },
        { text: 'Departamento de origen', value: 'Nombre_departamento' },
        { text: 'Foto', value: 'Foto_candidato' },
        { text: 'Hoja de vida', value: 'Hoja_de_vida_candidato' },
        { text: 'Propuesta', value: 'Propuesta_candidato' },
        { text: 'Acciones', value: 'actions', sortable: false },
      ],
      candidatos: [],
      editedIndex: -1,
      editedItem: {
        ID_candidato: '',
        ID_candidato_elector: '',
        DNI_candidato_elector: '',
        ID_partido_politico: '',
        Nombre_candidato_elector:'',
        Apellidos_candidato_elector: '',
        Foto_candidato: '',
        Hoja_de_vida_candidato: '',
        Propuesta_candidato: '',
        Nombre_departamento: '',
      },
      defaultItem: {
        ID_candidato: '',
        ID_candidato_elector: '',
        DNI_candidato_elector: '',
        ID_partido_politico: '',
        Nombre_candidato_elector:'',
        Apellidos_candidato_elector: '',
        Foto_candidato: '',
        Hoja_de_vida_candidato: '',
        Propuesta_candidato: '',
        Nombre_departamento: '',
      },
    }),

    computed: {
      formCandidato () {
        return this.editedIndex === -1 ? 'Nuevo candidato' : 'Editar candidato'
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
        this.candidatos = [
            {
            ID_elector : "sha45ty929",
            DNI_elector : 76918799,
            Nombre_elector : "Fabricio",
            Apellidos_elector : "Centeno",
            Estado_elector : "0",
            Tipo_elector : "elector",
            Direccion_elector : "Urb. Crisantemos",
            Departamento_elector : "Arequipa",
            Email_elector : "rcentenoc@gmail.com",
            Telefono_elector : "989131389",
            Nacimiento_elector : "1997-10-28",
            Genero_elector : "Masculino",
            Password_elector : "4587541213",
            ID_ubigeo_elector : "040101",
            vector_elector :"0.154632"
          },
        ]
      },

      getItems () {
        axios.get(url, {
          headers: this.config_request
        })
        .then(response => {
          this.candidatos = response.data
        })
        .catch(error => {
          console.log(error)
        })
      },

      actionEdit (item) {
        this.editedIndex = this.candidatos.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.candidatos.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(url + '/' + this.editedItem.ID_candidato, {
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
          this.candidatos.push(response.data)
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
        // this.candidatos.push(this.editedItem)
      },

      editItem (){
        axios.put(url+'/editar/'+this.editedItem.ID_candidato, this.editedItem, {
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
          // Object.assign(this.candidatos[this.editedIndex], this.editedItem)
        } else {
          console.log("crear")
          this.addItem()
          // this.candidatos.push(this.editedItem)
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

