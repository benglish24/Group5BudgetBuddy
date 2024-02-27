import {createContext, useState, useEffect} from 'react'
import {jwtDecode} from 'jwt-decode'

/* 
This file takes is for handling tokens. 
*/

import {useRouter} from 'next/router'

const AuthContext = createContext()
export default AuthContext

export const AuthProvider = ({ children }) => {

    const [authTokens, setAuthTokens] = useState(() => 
        typeof window !== "undefined" && localStorage.getItem("authTokens") // can't access localStorage 
        ? JSON.parse(localStorage.getItem("auth")) 
        : null
    );
    
    const [user, setUser] = useState(() => 
        typeof window !== "undefined" && localStorage.getItem("authTokens") 
        ? jwtDecode(localStorage.getItem("authTokens"))
        : null
    );

    const [loading, setLoading] = useState(true)
    const router = useRouter()

    const loginUser = async (username, password) => {
        const response = await fetch("http://localhost:8000/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username, password
            })
        })

        const data = await response.json()
        console.log(data)

        if (response.status === 200) {
            console.log("Logged in")
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            if (typeof window !== "undefined") {
                localStorage.setItem("authTokens", JSON.stringify(data))
            }
            router.push("/dashboard")
        } else {
            console.log(response.status)
            alert("Login failed.", response.status)
        }
    }

    const registerUser = async (username, password, confirm_password) => {
        const response = await fetch("http://localhost:8000/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username, password, confirm_password
            })
        })

        if (response.status === 201) {
            router.push("/")
            loginUser(username, password)
        } else {
            console.log(response.status)
            console.log("There was a server issue", response.status, response)
            alert("Registration failed.", response.status)
        }

    }

    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        
        if (typeof window !== "undefined") {
            localStorage.removeItem("authTokens")
        }
        console.log("USER LOGGED OUT", authTokens, user)
        router.push("/")
    }

    const contextData = {
        user,
        setUser,
        authTokens,
        setAuthTokens,
        registerUser,
        loginUser,
        logoutUser
    }

    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access))
        }
        setLoading(false)
    }, [authTokens, loading])

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children} 
        </AuthContext.Provider>
    )
}
