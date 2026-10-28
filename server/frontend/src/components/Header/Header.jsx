import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = () => {
  const logout = async (e) => {
    e.preventDefault();
    let logout_url = window.location.origin + "/djangoapp/logout";
    const res = await fetch(logout_url, {
      method: "GET",
    });

    const json = await res.json();
    if (json) {
      let username = sessionStorage.getItem('username');
      sessionStorage.removeItem('username');
      alert("Logging out " + (username || "") + "...");
      window.location.href = window.location.origin;
    } else {
      alert("The user could not be logged out.");
    }
  };

  let curr_user = sessionStorage.getItem('username');
  let home_page_items = (
    <div className="input_panel" style={{ display: "flex", alignItems: "center" }}>
      <a className="nav_item" style={{ fontSize: "larger", marginRight: "15px", textDecoration: "none" }} href="/login">Login</a>
      <a className="nav_item" style={{ fontSize: "larger", textDecoration: "none" }} href="/register">Register</a>
    </div>
  );

  if (curr_user !== null && curr_user !== "") {
    home_page_items = (
      <div className="input_panel" style={{ display: "flex", alignItems: "center" }}>
        <span className="username" style={{ fontSize: "larger", marginRight: "15px", fontWeight: "bold", color: "#333" }}>{curr_user}</span>
        <a className="nav_item btn btn-outline-dark btn-sm" href="/djangoapp/logout" onClick={logout}>Logout</a>
      </div>
    );
  }

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: "darkturquoise", height: "1in" }}>
        <div className="container-fluid">
          <h2 style={{ paddingRight: "5%", margin: 0, fontWeight: "bold" }}>Dealerships</h2>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarText">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/about">About Us</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/contact">Contact Us</a>
              </li>
            </ul>
            <span className="navbar-text">
              <div className="loginlink" id="loginlogout">
                {home_page_items}
              </div>
            </span>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Header;
