<template>
    
  <v-data-table :headers="headers" :items="electores" sort-by="Apellidos_elector" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
      <v-toolbar-title class="subheading blue--text">ELECTORES</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="500px">

          <template v-slot:activator="{ on, attrs }">
            
            <v-btn color="blue" dark class="mb-2" v-bind="attrs" v-on="on">
              Agregar elector
            </v-btn>

          </template>

          <v-card>
            <v-card-title>
              <span class="text-h5 blue--text">{{ formElector }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_elector"
                      label="ID del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.DNI_elector"
                      label="DNI del elector"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Nombre_elector"
                      label="Nombre del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Apellidos_elector"
                      label="Apellido del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Estado_elector"
                      label="Estado del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Tipo_elector"
                      label="Tipo de elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Direccion_elector"
                      label="Dirección del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Departamento_elector"
                      label="Departamento del elector"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="12">
                    <v-text-field v-model="editedItem.Email_elector"
                      label="Email del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Telefono_elector"
                      label="Teléfono del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Nacimiento_elector"
                      label="Fecha de nacimiento del elector"
                      hint="YYYY/MM/DD format"
                      persistent 
                      prepend-icon="event" 
                      @blur="date = parseDate(dateFormatted)" 
                      v-on="on">
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Genero_elector"
                      label="Género del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.Password_elector"
                      label="Password del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.ID_ubigeo_elector"
                      label="Ubigeo del elector"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="6">
                    <v-text-field v-model="editedItem.vector_elector"
                      label="Vector de reconocimiento del elector"
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
  var url = 'http://127.0.0.1:5000/elector';
  export default {
    data: () => ({
      config_request: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
      },          
      dialog: false,
      dialogDelete: false,
      headers: [
        { text: 'ID', value: 'ID_elector' },
        { text: 'DNI', value: 'DNI_elector' },
        { text: 'Apellidos', value: 'Apellidos_elector' },
        { text: 'Nombre', value: 'Nombre_elector' },
        { text: 'Tipo', value: 'Tipo_elector' },
        { text: 'Dirección', value: 'Direccion_elector' },
        { text: 'Departamento', value: 'Departamento_elector' },
        { text: 'Email', value: 'Email_elector' },
        { text: 'Telefono', value: 'Telefono_elector' },
        { text: 'Nacimiento', value: 'Nacimiento_elector' },
        { text: 'Genero', value: 'Genero_elector' },
        { text: 'Password', value: 'Password_elector' },
        { text: 'Estado de votación', value: 'Estado_elector' },
        { text: 'Ubigeo', value: 'ID_ubigeo_elector' },
        { text: 'Vector', value: 'vector_elector' },
        { text: 'Acciones', value: 'actions', sortable: false },
      ],
      electores: [],
      editedIndex: -1,
      editedItem: {
        ID_elector: '',
        DNI_elector: '',
        Nombre_elector: '',
        Apellidos_elector: '',
        Estado_elector: 0,
        Tipo_elector: 'Elector',
        Email_elector: '',
        Telefono_elector: '',
        Nacimiento_elector: '',
        Genero_elector: '',
        Password_elector: '',
        Direccion_elector: '',
        Departamento_elector: '',
        ID_ubigeo_elector: '',
        vector_elector: '',
      },
      defaultItem: {
        ID_elector: '',
        DNI_elector: '',
        Nombre_elector: '',
        Apellidos_elector: '',
        Estado_elector: 0,
        Tipo_elector: 'Elector',
        Email_elector: '',
        Telefono_elector: '',
        Nacimiento_elector: '',
        Genero_elector: '',
        Password_elector: '',
        Direccion_elector: '',
        Departamento_elector: '',
        ID_ubigeo_elector: '',
        vector_elector: '',
      },
    }),

    computed: {
      formElector () {
        return this.editedIndex === -1 ? 'Nuevo elector' : 'Editar elector'
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
        this.electores = [
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
          {
            ID_elector : "sha40ty356",
            DNI_elector : "26568789",
            Nombre_elector : "Silvip",
            Apellidos_elector : "Rodriguez",
            Estado_elector : "0",
            Tipo_elector : "Elector",
            Direccion_elector : "Urb. Velasco Astete S-15",
            Departamento_elector : "Ica",
            Email_elector : "sroduiguez@gmail.com",
            Telefono_elector : "945687856",
            Nacimiento_elector : "1950-01-20",
            Genero_elector : "Masculino",
            Password_elector : "568795456",
            ID_ubigeo_elector : "110102",
            vector_elector :"0.154632"
          },
        ]
      },

      getItems () {
        axios.get(url, {
          headers: this.config_request
        })
        .then(response => {
          this.electores = response.data
        })
        .catch(error => {
          console.log(error)
        })
      },

      actionEdit (item) {
        this.editedIndex = this.electores.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.electores.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        axios.delete(url + '/' + this.editedItem.ID_elector, {
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
          this.electores.push(response.data)
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
        // this.electores.push(this.editedItem)
      },

      editItem (){
        axios.put(url+'/editar/'+this.editedItem.ID_elector, this.editedItem, {
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
          // Object.assign(this.electores[this.editedIndex], this.editedItem)
        } else {
          console.log("crear")
          this.addItem()
          // this.electores.push(this.editedItem)
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

