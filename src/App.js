import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './pages/landing';
import SignIn from './pages/signin';
import SignUp from './pages/signup';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Home from './pages/home';
import Create from './pages/create';
import Topics from './pages/topics';
import Course from './pages/course';

function App() {

  return (
    <Router>
      <div>
        <ToastContainer
          limit={3}
          progressClassName={sessionStorage.getItem('darkMode') === 'true' ? "toastProgressDark" : "toastProgress"}
          bodyClassName={sessionStorage.getItem('darkMode') === 'true' ? "toastBodyDark" : "toastBody"}
          position="bottom-center"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme={sessionStorage.getItem('darkMode') === 'true' ? 'dark' : 'light'}
        />
        <Routes>
          <Route path="/" exact element={<Landing />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path='/home' element={<Home />} />
          <Route path='/create' element={<Create />} />
          <Route path='/topics' element={<Topics />} />
          <Route path='/course' element={<Course />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
