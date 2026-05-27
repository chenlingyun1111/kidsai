import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../data/auth_repository.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _pinController = TextEditingController();
  final _nameController = TextEditingController();
  final _auth = AuthRepository();
  bool _isLogin = true;
  bool _loading = false;
  String? _error;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 60),
              Text('KidsAI',
                  style: Theme.of(context)
                      .textTheme
                      .headlineLarge
                      ?.copyWith(color: Theme.of(context).colorScheme.primary)),
              const SizedBox(height: 8),
              Text(_isLogin ? 'Welcome back!' : 'Create an account',
                  style: Theme.of(context).textTheme.bodyLarge),
              const SizedBox(height: 48),
              if (!_isLogin)
                TextField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: 'Display Name',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person),
                  ),
                ),
              if (!_isLogin) const SizedBox(height: 16),
              TextField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.email),
                ),
                keyboardType: TextInputType.emailAddress,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
                obscureText: true,
              ),
              if (!_isLogin) const SizedBox(height: 16),
              if (!_isLogin)
                TextField(
                  controller: _pinController,
                  decoration: const InputDecoration(
                    labelText: 'Parent PIN (4 digits)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.pin),
                  ),
                  keyboardType: TextInputType.number,
                  maxLength: 4,
                  obscureText: true,
                ),
              if (_error != null)
                Padding(
                  padding: const EdgeInsets.only(top: 16),
                  child: Text(_error!,
                      style: TextStyle(color: Theme.of(context).colorScheme.error)),
                ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _submit,
                  child: _loading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2))
                      : Text(_isLogin ? 'Login' : 'Register'),
                ),
              ),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () => setState(() {
                  _isLogin = !_isLogin;
                  _error = null;
                }),
                child: Text(_isLogin
                    ? "Don't have an account? Register"
                    : 'Already have an account? Login'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      if (_isLogin) {
        await _auth.login(
          email: _emailController.text.trim(),
          password: _passwordController.text,
        );
      } else {
        await _auth.register(
          email: _emailController.text.trim(),
          password: _passwordController.text,
          pin: _pinController.text,
          displayName: _nameController.text.trim(),
        );
      }
      if (mounted) context.go('/characters');
    } catch (e) {
      setState(() => _error = 'Failed. Please check your input.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _pinController.dispose();
    _nameController.dispose();
    super.dispose();
  }
}
