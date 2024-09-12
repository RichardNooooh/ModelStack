import {
    createBrowserRouter,
    createRoutesFromElements,
    Route,
    RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={<div>Hello World from router</div>}
      // loader={}
      // action={}
      // errorElement={}
    >

    </Route>
  )
);

export default function App() {
  return (<RouterProvider router={router}/>)
}
