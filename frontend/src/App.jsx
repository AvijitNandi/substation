import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

axios.defaults.withCredentials = true

function getCookie(name) {
  const cookies = document.cookie.split(';')

  for (const cookie of cookies) {
    const [key, value] = cookie.trim().split('=')

    if (key === name) {
      return decodeURIComponent(value)
    }
  }

  return null
}

const API = 'http://localhost:8000/api'

function App() {
  const [substations, setSubstations] = useState([])
  const [inspectionTypes, setInspectionTypes] = useState([])

  const [formData, setFormData] = useState({
    report_no: '',
    inspection_date: '',
    substation: '',
    inspection_type: '',
    peak_load_mw: '',
    general_comment: '',
  })

  useEffect(() => {
    axios
      .get(`${API}/substations/`)
      .then((response) => {
        console.log('SUBSTATIONS:', response.data)
        setSubstations(response.data.results)
      })
      .catch((error) => {
        console.error('Substation API error:', error)
      })

    axios
      .get(`${API}/inspection-types/`)
      .then((response) => {
        setInspectionTypes(response.data.results)
      })
      .catch((error) => {
        console.error('Inspection Type API error:', error)
      })
  }, [])

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData({
      ...formData,
      [name]: value,
    })
  }

  const handleSubmit = async () => {
      if (!formData.report_no.trim()) {
      alert('Report No. is required.')
      return
    }

    if (!formData.inspection_date) {
      alert('Inspection Date is required.')
      return
    }

    if (!formData.substation) {
      alert('Please select a Substation.')
      return
    }

    if (!formData.inspection_type) {
      alert('Please select an Inspection Type.')
      return
    }
    try {
      await axios.get(`${API}/csrf/`)

      const payload = {
        report_no: formData.report_no,
        inspection_date: formData.inspection_date,
        peak_load_mw: formData.peak_load_mw || null,
        general_comment: formData.general_comment,
        substation: Number(formData.substation),
        inspection_type: Number(formData.inspection_type),
      }

      const response = await axios.post(
          `${API}/inspection-reports/`,
          payload,
          {
            headers: {
              'X-CSRFToken': getCookie('csrftoken'),
            },
          }
        )

      console.log('Report created:', response.data)

      alert('Inspection Report saved successfully!')

      setFormData({
        report_no: '',
        inspection_date: '',
        substation: '',
        inspection_type: '',
        peak_load_mw: '',
        general_comment: '',
      })

    } catch (error) {
      console.error('Report save error:', error.response?.data || error)
      alert('Failed to save report.')
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>BREB Substation Inspection System</h1>
        <p>Bangladesh Rural Electrification Board</p>
      </header>

      <main className="container">
        <section className="card">
          <h2>Inspection Report</h2>

          <div className="form-grid">
            <div>
              <label>Report No.</label>
              <input
                type="text"
                name="report_no"
                value={formData.report_no}
                onChange={handleChange}
                placeholder="Enter report number"
              />
            </div>

            <div>
              <label>Inspection Date</label>
              <input
                type="date"
                name="inspection_date"
                value={formData.inspection_date}
                onChange={handleChange}
              />
            </div>

            <div>
              <label>Substation</label>
              <select
                name="substation"
                value={formData.substation}
                onChange={handleChange}
              >
                <option value="">Select Substation</option>

                {substations.map((substation) => (
                  <option key={substation.id} value={substation.id}>
                    {substation.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label>Inspection Type</label>
              <select
                name="inspection_type"
                value={formData.inspection_type}
                onChange={handleChange}
              >
                <option value="">Select Inspection Type</option>

                {inspectionTypes.map((type) => (
                  <option key={type.id} value={type.id}>
                    {type.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label>Peak Load (MW)</label>
              <input
                type="number"
                step="0.01"
                name="peak_load_mw"
                value={formData.peak_load_mw}
                onChange={handleChange}
                placeholder="0.00"
              />
            </div>

            <div>
              <label>Status</label>
              <input
                type="text"
                value="DRAFT"
                readOnly
              />
            </div>
          </div>

          <div className="full-width">
            <label>General Comment</label>
            <textarea
              rows="4"
              name="general_comment"
              value={formData.general_comment}
              onChange={handleChange}
              placeholder="Enter general comment"
            ></textarea>
          </div>

          <button type="button" onClick={handleSubmit}>
            Save Draft
          </button>
        </section>
      </main>
    </div>
  )
}

export default App