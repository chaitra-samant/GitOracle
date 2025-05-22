import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="bg-primary text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">RAG System</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="hover:text-secondary transition-colors">
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/app"
                className="hover:text-secondary transition-colors"
              >
                App
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
