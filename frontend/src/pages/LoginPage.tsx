import { Link } from "react-router-dom";

export default function LoginPage() {
  return (
    <div className="font-sans min-h-screen antialiased bg-gradient-to-tr from-gray-900 to-green-800 pt-24 pb-5">
      <div className="flex flex-col justify-center sm:w-96 sm:mx-auto mx-5 mb-5 space-y-8">
        <h1 className="font-bold text-center text-4xl text-yellow-500">
          Administrar <span className="text-blue-500">Cepas</span>
        </h1>
        <form action="#" method="post">
          <div className="flex flex-col bg-white p-10 rounded-lg shadow space-y-6">
            <h1 className="font-bold text-xl text-center">
              Inicia sesión para continuar
            </h1>

            <div className="flex flex-col space-y-1">
              <input
                type="text"
                name="username"
                id="username"
                placeholder="Nombre de usuario"
                className="border-2 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-400 focus:shadow"
                required
              />
            </div>

            <div className="flex flex-col space-y-1">
              <input
                type="password"
                name="password"
                id="password"
                placeholder="Contraseña"
                className="border-2 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-400 focus:shadow"
                required
              />
            </div>

            <div className="relative flex items-center">
              <input
                type="checkbox"
                name="remember"
                id="remember"
                defaultChecked
                className="inline-block align-middle"
              />
              <label
                htmlFor="remember"
                className="inline-block align-middle ml-2 text-gray-700"
              >
                Recordar datos
              </label>
            </div>

            <div className="flex flex-col-reverse sm:flex-row sm:justify-between items-center">
              <a
                href="#"
                className="inline-block text-blue-500 hover:text-blue-800 hover:underline mt-3 sm:mt-0"
              >
                Ingresar como invitado
              </a>
              <Link to="/home">
                <button className="text-white">Aceptar</button>
              </Link>
            </div>
          </div>
        </form>
        <div className="flex justify-center text-gray-500 text-sm">
          <p>&copy;2025, SM. Todos los derechos reservados.</p>
        </div>
      </div>
    </div>
  );
}
